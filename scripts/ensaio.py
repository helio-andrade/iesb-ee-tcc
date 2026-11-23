"""Fase 3 — bateria de ensaio de desempenho de uma etapa (mesmo script para todas as etapas).

Uso:
  python ensaio.py --projeto TCC-etapa-0 --etapa 0 --reps 30
  python ensaio.py --projeto TCC-etapa-0 --etapa 0 --reps 1 --teste     (validação rápida)

Em cada repetição, para cada caminho:
  - latência: fping -C 20 -p 100 -t 1000 (média, p95, perda; -t explícito: com -C o padrão do timeout é o intervalo)
  - TCP: iperf3 10 s (vazão, retransmissões)
  - UDP: iperf3 5 s a 90% da capacidade do caminho, pacotes de 64, 512, 1024 e 1400 bytes (vazão, jitter, perda)
  - CPU e memória de cada equipamento durante o teste (lidos na GNS3 VM: /proc dos processos QEMU/IOL e
    cgroup cpuacct dos contêineres), em % de 1 núcleo e MB.
  - carga do ambiente durante o teste (ambiente.csv): CPU total e steal da GNS3 VM (/proc/stat), carga média
    (/proc/loadavg) e CPU do Windows (GetSystemTimes) — para separar efeito da etapa de interferência externa.
Antes da bateria: --aquecer N repetições completas descartadas (padrão 1), para não medir tarefas de inicialização.
Saída: lab/dados/ensaios/etapa-<etapa>/  resultados.csv, cpu.csv, ambiente.csv, bruto.jsonl, meta.json
O script retoma de onde parou (pula repetições já gravadas em resultados.csv).
Regra: durante a bateria, nada no computador nem no projeto (interface do GNS3, consoles, outros scripts).
"""
import argparse, csv, ctypes, datetime, json, os, pathlib, re, statistics, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import gns3lab as g

ap = argparse.ArgumentParser()
ap.add_argument('--projeto', required=True); ap.add_argument('--etapa', required=True)
ap.add_argument('--reps', type=int, default=30); ap.add_argument('--teste', action='store_true')
ap.add_argument('--aquecer', type=int, default=1, help='repetições descartadas antes da bateria')
ap.add_argument('--portal', help='etapas B: autentica a PC-USUARIO no portal cativo antes de medir, "usuario:senha@url"')
A = ap.parse_args()

def log(*a): print(time.strftime('%H:%M:%S'), *a, flush=True)
RAIZ = pathlib.Path(__file__).resolve().parents[1]
SAIDA = RAIZ / 'dados' / 'ensaios' / (f'etapa-{A.etapa}' + ('-teste' if A.teste else ''))
SAIDA.mkdir(parents=True, exist_ok=True)

# caminhos: nome -> (origem, destino, ip destino, capacidade nominal Mbit/s)
CAMINHOS = {
    'LAN-matriz':     ('PC-USUARIO', 'APLICACAO', '10.10.10.21', 100),
    'matriz-filial1': ('PC-USUARIO', 'PC-FIL1',   '10.20.10.11', 20),
    'matriz-filial2': ('PC-USUARIO', 'PC-FIL2',   '10.30.10.11', 10),
    'filial1-filial2':('PC-FIL1',    'PC-FIL2',   '10.30.10.11', 10),
}
TAMANHOS = [64, 512, 1024, 1400]          # tamanho do pacote IP (bytes); payload UDP = tamanho - 28
FRACAO_UDP = 0.9
EQUIP = ['R-HQ', 'R-FIL1', 'R-FIL2', 'FW-HQ', 'FW-F1', 'FW-F2', 'SW-CORE', 'SW-ACC1', 'SW-ACC2', 'SW-FIL1', 'SW-FIL2', 'PROVEDOR']

p = g.Projeto(A.projeto)
nos = {n['name']: n for n in g.api('GET', f'/projects/{p.id}/nodes')}
cont = {h: g.conteiner(p, nos[h]) for h in {c[0] for c in CAMINHOS.values()} | {c[1] for c in CAMINHOS.values()}}
# o IP de destino é lido do próprio contêiner: muda entre etapas (APLICACAO: 10.10.10.21 na etapa 0, 10.10.20.21 a partir da A)
for nome, (o, d, _, cap) in list(CAMINHOS.items()):
    ip_d = g.vm(f"docker exec {cont[d]} ip -4 -o addr show eth0").split()[3].split('/')[0]
    CAMINHOS[nome] = (o, d, ip_d, cap)

# ---------------------------------------------------------------- mapa equipamento -> fonte de CPU/memória
def mapear():
    m = {}
    iol = {}
    for linha in g.vm('for p in $(pgrep -f "[.]iol"); do echo $p $(sudo -n readlink /proc/$p/cwd); done').splitlines():
        partes = linha.split()
        if len(partes) == 2:
            iol[partes[1].rstrip('/').split('/')[-1]] = partes[0]
    for e in EQUIP:
        n = nos[e]
        if n['node_type'] == 'qemu':
            pid = g.vm(f"ps -eo pid,args | grep '[q]emu-system-x86_64 -name {e} ' | awk '{{print $1}}' | head -1").strip()
            m[e] = ('pid', pid)
        elif n['node_type'] == 'iou':
            m[e] = ('pid', iol.get(n['node_id'], ''))
        elif n['node_type'] == 'docker':
            m[e] = ('cg', g.conteiner(p, n))
    return m
MAPA = mapear()
faltando = [e for e, (t, v) in MAPA.items() if not v]
if faltando:
    raise SystemExit(f'sem processo para: {faltando}')
CMD_SNAP = ' ; '.join(
    (f"echo {e} $(awk '{{print $14+$15}}' /proc/{v}/stat) $(awk '/VmRSS/{{print $2}}' /proc/{v}/status)" if t == 'pid' else
     f"echo {e} $(( $(cat /sys/fs/cgroup/cpuacct/docker/{v}/cpuacct.usage) / 10000000 )) $(( $(cat /sys/fs/cgroup/memory/docker/{v}/memory.usage_in_bytes) / 1024 ))")
    for e, (t, v) in MAPA.items()) + " ; echo __VM $(head -1 /proc/stat) ; echo __LOAD $(cat /proc/loadavg)"


class _FT(ctypes.Structure):
    _fields_ = [('lo', ctypes.c_uint32), ('hi', ctypes.c_uint32)]


def host_tempos():
    """(ocioso, total) do Windows em unidades de 100 ns (GetSystemTimes; kernel inclui o ocioso)."""
    if os.name != 'nt':
        return None
    i, k, u = _FT(), _FT(), _FT()
    if not ctypes.windll.kernel32.GetSystemTimes(ctypes.byref(i), ctypes.byref(k), ctypes.byref(u)):
        return None
    v = lambda f: (f.hi << 32) | f.lo
    return v(i), v(k) + v(u)


def snapshot():
    r = {}
    for linha in g.vm(CMD_SNAP).splitlines():
        partes = linha.split()
        if partes[:1] == ['__VM']:
            r['__VM'] = [int(x) for x in partes[2:10]]          # user nice system idle iowait irq softirq steal
        elif partes[:1] == ['__LOAD']:
            r['__LOAD'] = float(partes[1])
        elif len(partes) == 3:
            r[partes[0]] = (int(partes[1]), int(partes[2]))     # ticks (1/100 s), memória KB
    r['__HOST'] = host_tempos()
    return r, time.time()

# ---------------------------------------------------------------- preparação
pv = g.conteiner(p, nos['PROVEDOR'])
if 'netem' not in g.vm(f'docker exec {pv} tc qdisc show dev eth1'):
    log('perfis de enlace ausentes no PROVEDOR; reaplicando:', g.vm(f'docker exec {pv} sh /etc/network/provedor.sh').strip()[-20:])
for h in {c[1] for c in CAMINHOS.values()}:
    g.vm(f'docker exec {cont[h]} sh -c "killall iperf3 2>/dev/null; iperf3 -s -D"')
if A.portal:
    # etapas Zero Trust: sem sessão no portal cativo, o usuário não alcança o enclave nem as filiais
    cred, url = A.portal.rsplit('@', 1); usu, sen = cred.split(':', 1)
    r = g.vm(f"docker exec {cont['PC-USUARIO']} curl -s -m 15 -X POST -d 'user={usu}&password={sen}' {url}")
    if 'authenticated_via' not in r and 'AUTHORIZED' not in r.replace('NOT_AUTHORIZED', ''):
        raise SystemExit('login no portal falhou: ' + r[:200])
    log('PC-USUARIO autenticada no portal cativo')
time.sleep(1)

feitas = set()
ARQ_RES = SAIDA / 'resultados.csv'
if ARQ_RES.exists():
    with open(ARQ_RES, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            feitas.add(int(row['rep']))
CAMPOS = ['etapa', 'rep', 'data_hora', 'caminho', 'teste', 'tamanho_bytes', 'taxa_oferecida_mbps',
          'vazao_mbps', 'retrans', 'jitter_ms', 'perda_pct', 'rtt_medio_ms', 'rtt_p95_ms', 'rtt_min_ms', 'rtt_max_ms']
novo_res = not ARQ_RES.exists()
fres = open(ARQ_RES, 'a', newline='', encoding='utf-8'); wres = csv.DictWriter(fres, CAMPOS)
if novo_res: wres.writeheader()
ARQ_CPU = SAIDA / 'cpu.csv'; novo_cpu = not ARQ_CPU.exists()
fcpu = open(ARQ_CPU, 'a', newline='', encoding='utf-8'); wcpu = csv.writer(fcpu)
if novo_cpu: wcpu.writerow(['etapa', 'rep', 'caminho', 'teste', 'tamanho_bytes', 'equipamento', 'cpu_pct_1nucleo', 'memoria_mb'])
ARQ_AMB = SAIDA / 'ambiente.csv'; novo_amb = not ARQ_AMB.exists()
famb = open(ARQ_AMB, 'a', newline='', encoding='utf-8'); wamb = csv.writer(famb)
if novo_amb: wamb.writerow(['etapa', 'rep', 'caminho', 'teste', 'tamanho_bytes', 'vm_cpu_pct', 'vm_steal_pct', 'vm_carga_1min', 'host_cpu_pct'])
fbruto = open(SAIDA / 'bruto.jsonl', 'a', encoding='utf-8')
(SAIDA / 'meta.json').write_text(json.dumps({
    'projeto': A.projeto, 'etapa': A.etapa, 'repeticoes': A.reps, 'caminhos': CAMINHOS, 'tamanhos_bytes': TAMANHOS,
    'fracao_udp': FRACAO_UDP, 'equipamentos': EQUIP, 'mapa_cpu': MAPA,
    'metodo': {'latencia': 'fping -C 20 -p 100 -t 1000 -q', 'tcp': 'iperf3 -t 10 -J', 'udp': 'iperf3 -u -b <90% cap> -l <tam-28> -t 5 -J',
               'cpu': 'delta (utime+stime) de /proc/<pid>/stat (QEMU, IOL) ou cpuacct.usage do cgroup (contêineres) / delta t, % de 1 núcleo',
               'ambiente': 'GNS3 VM: delta de /proc/stat (CPU ocupada e steal, % de todos os núcleos) e /proc/loadavg; Windows: GetSystemTimes (% de todos os núcleos)'},
    'aquecimento_reps': A.aquecer,
}, indent=1, ensure_ascii=False), encoding='utf-8')

GRAVAR = True   # False durante o aquecimento


def medir_cpu(rep, caminho, teste, tam, antes, depois):
    if not GRAVAR:
        return
    (a, ta), (b, tb) = antes, depois
    for e in EQUIP:
        if e in a and e in b:
            wcpu.writerow([A.etapa, rep, caminho, teste, tam, e, f'{(b[e][0]-a[e][0])/100/(tb-ta)*100:.1f}', f'{b[e][1]/1024:.0f}'])
    vm_cpu = vm_steal = host = ''
    if '__VM' in a and '__VM' in b:
        d = [y - x for x, y in zip(a['__VM'], b['__VM'])]
        tot = sum(d)
        if tot > 0:
            vm_cpu = f'{100 * (tot - d[3] - d[4]) / tot:.1f}'      # tudo menos idle e iowait
            vm_steal = f'{100 * d[7] / tot:.1f}'
    if a.get('__HOST') and b.get('__HOST'):
        di, dt = b['__HOST'][0] - a['__HOST'][0], b['__HOST'][1] - a['__HOST'][1]
        if dt > 0:
            host = f'{100 * (dt - di) / dt:.1f}'
    wamb.writerow([A.etapa, rep, caminho, teste, tam, vm_cpu, vm_steal, b.get('__LOAD', ''), host])


def escrever(arq, texto):
    if GRAVAR:
        arq.write(texto)


def linha(rep, caminho, teste, tam='', taxa='', **v):
    if not GRAVAR:
        return
    row = dict(etapa=A.etapa, rep=rep, data_hora=datetime.datetime.now().isoformat(timespec='seconds'), caminho=caminho,
               teste=teste, tamanho_bytes=tam, taxa_oferecida_mbps=taxa)
    row.update({k: (f'{x:.3f}' if isinstance(x, float) else x) for k, x in v.items()})
    wres.writerow(row)

def iperf(o, ip, args, t):
    j = g.vm(f'docker exec {cont[o]} timeout {t+20} iperf3 -c {ip} {args} -J', t + 40)
    try:
        return json.loads(j[j.find('{'):]), j
    except Exception:
        return None, j

# ---------------------------------------------------------------- bateria
def repeticao(rep):
    for nome, (o, d, ip, cap) in CAMINHOS.items():
        # latência
        antes = snapshot()
        out = g.vm(f'docker exec {cont[o]} fping -C 20 -p 100 -t 1000 -q {ip} 2>&1')
        depois = snapshot()
        vals = [float(x) for x in re.findall(r'\b\d+\.\d+\b', out.split(':', 1)[-1])]
        perdidos = out.split(':', 1)[-1].count('-')
        if vals:
            vs = sorted(vals)
            linha(rep, nome, 'latencia', rtt_medio_ms=statistics.mean(vals), rtt_p95_ms=vs[max(0, int(round(0.95 * len(vs))) - 1)],
                  rtt_min_ms=vs[0], rtt_max_ms=vs[-1], perda_pct=100.0 * perdidos / 20)
        else:
            linha(rep, nome, 'latencia', perda_pct=100.0)
        medir_cpu(rep, nome, 'latencia', '', antes, depois)
        escrever(fbruto, json.dumps({'rep': rep, 'caminho': nome, 'teste': 'latencia', 'saida': out}) + '\n')
        # TCP
        antes = snapshot(); d_tcp, bruto = iperf(o, ip, '-t 10', 10); depois = snapshot()
        if d_tcp and 'end' in d_tcp and 'sum_received' in d_tcp['end']:
            e = d_tcp['end']
            linha(rep, nome, 'tcp', vazao_mbps=e['sum_received']['bits_per_second'] / 1e6, retrans=e['sum_sent'].get('retransmits'))
        else:
            linha(rep, nome, 'tcp', vazao_mbps=0.0)
        medir_cpu(rep, nome, 'tcp', '', antes, depois)
        escrever(fbruto, json.dumps({'rep': rep, 'caminho': nome, 'teste': 'tcp', 'iperf': d_tcp or bruto[-500:]}) + '\n')
        # UDP por tamanho
        taxa = cap * FRACAO_UDP
        for tam in TAMANHOS:
            antes = snapshot(); d_udp, bruto = iperf(o, ip, f'-u -b {taxa}M -l {tam-28} -t 5', 5); depois = snapshot()
            if d_udp and 'end' in d_udp and 'sum' in d_udp['end']:
                s = d_udp['end']['sum']
                linha(rep, nome, 'udp', tam, taxa, vazao_mbps=s.get('bits_per_second', 0) / 1e6 * (1 - s.get('lost_percent', 0) / 100),
                      jitter_ms=s.get('jitter_ms', 0.0), perda_pct=s.get('lost_percent', 0.0))
            else:
                linha(rep, nome, 'udp', tam, taxa, vazao_mbps=0.0, perda_pct=100.0)
            medir_cpu(rep, nome, 'udp', tam, antes, depois)
            escrever(fbruto, json.dumps({'rep': rep, 'caminho': nome, 'teste': 'udp', 'tamanho': tam, 'iperf': d_udp or bruto[-500:]}) + '\n')
        fres.flush(); fcpu.flush(); famb.flush(); fbruto.flush()


reps = range(1, A.reps + 1)
t_ini = time.time()
pendentes = [r for r in reps if r not in feitas]
if pendentes and A.aquecer > 0:
    GRAVAR = False
    for k in range(1, A.aquecer + 1):
        t0 = time.time(); repeticao(0)
        log(f'aquecimento {k}/{A.aquecer} (descartado) em {time.time() - t0:.0f} s')
    GRAVAR = True
for rep in pendentes:
    t_rep = time.time()
    repeticao(rep)
    dur = time.time() - t_rep
    restantes = len([r for r in pendentes if r > rep])
    log(f'repetição {rep}/{A.reps} concluída em {dur:.0f} s; faltam ~{restantes * dur / 60:.0f} min')
fres.close(); fcpu.close(); famb.close(); fbruto.close()
log(f'bateria da etapa {A.etapa} concluída em {(time.time()-t_ini)/60:.1f} min; dados em {SAIDA}')
