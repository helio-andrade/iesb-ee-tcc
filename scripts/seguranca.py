"""Métricas de segurança de uma etapa: superfície de ataque, alcance (movimentação lateral) e vulnerabilidades.

Uso: python seguranca.py --projeto TCC-etapa-0 --etapa 0 [--origens HOST-INVADIDO PC-FIL1]

Para cada origem (host considerado comprometido), a partir do próprio contêiner:
  1. Alcance de rede: nmap -sn sem ARP (eco ICMP + SYN/ACK em portas comuns) contra o inventário da etapa.
  2. Serviços: nmap -sS -sV nas 1000 portas TCP mais comuns (sem a 5201, servidor iperf3 do ensaio).
Depois, no Windows (independente da etapa e da saída do host para a internet):
  3. Vulnerabilidades: cada produto/versão encontrado é consultado na API pública do vulners.com (o mesmo banco do
     script vulners do Nmap), com cache em lab/dados/seguranca/vulners_cache.json; conta CVEs por severidade CVSS.
O provedor (172.16.0.x) e a rede do Windows/GNS3 VM (192.168.16.1 e .130) ficam fora: não são da empresa.
Saída: lab/dados/seguranca/etapa-<etapa>/  alcance.csv, servicos.csv, vulnerabilidades.csv, resumo.json, resumo.md, *.xml
"""
import argparse, csv, json, pathlib, sys, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import gns3lab as g

ap = argparse.ArgumentParser()
ap.add_argument('--projeto', required=True); ap.add_argument('--etapa', required=True)
ap.add_argument('--origens', nargs='+', default=['HOST-INVADIDO', 'PC-FIL1'])
ap.add_argument('--reanalisar', action='store_true', help='só recalcula o resumo a partir de alcance.csv e servicos.csv')
A = ap.parse_args()
RAIZ = pathlib.Path(__file__).resolve().parents[1]
SAIDA = RAIZ / 'dados' / 'seguranca' / f'etapa-{A.etapa}'; SAIDA.mkdir(parents=True, exist_ok=True)
CACHE = RAIZ / 'dados' / 'seguranca' / 'vulners_cache.json'
def log(*a): print(time.strftime('%H:%M:%S'), *a, flush=True)

# inventário: ip -> (equipamento, classe). Etapas seguintes acrescentam os IPs novos (VLANs, gerência).
INV_ETAPA0 = {
    '10.10.10.21': ('APLICACAO', 'servidor'), '10.10.10.22': ('ARQUIVOS', 'servidor'),
    '10.10.10.11': ('PC-USUARIO', 'estacao'), '10.10.10.12': ('HOST-INVADIDO', 'estacao'),
    '10.20.10.11': ('PC-FIL1', 'estacao'), '10.30.10.11': ('PC-FIL2', 'estacao'),
    '10.10.10.1': ('FW-HQ', 'firewall'), '10.255.1.2': ('FW-HQ', 'firewall'), '192.168.16.31': ('FW-HQ', 'firewall'),
    '10.20.10.1': ('FW-F1', 'firewall'), '10.255.2.2': ('FW-F1', 'firewall'), '192.168.16.32': ('FW-F1', 'firewall'),
    '10.30.10.1': ('FW-F2', 'firewall'), '10.255.3.2': ('FW-F2', 'firewall'), '192.168.16.33': ('FW-F2', 'firewall'),
    '10.255.1.1': ('R-HQ', 'roteador'), '172.16.0.2': ('R-HQ', 'roteador'),
    '10.255.2.1': ('R-FIL1', 'roteador'), '172.16.0.6': ('R-FIL1', 'roteador'),
    '10.255.3.1': ('R-FIL2', 'roteador'), '172.16.0.10': ('R-FIL2', 'roteador'),
    '10.10.10.2': ('SW-CORE', 'switch'), '10.10.10.3': ('SW-ACC1', 'switch'), '10.10.10.4': ('SW-ACC2', 'switch'),
    '10.20.10.2': ('SW-FIL1', 'switch'), '10.30.10.2': ('SW-FIL2', 'switch'),
}
# etapa A: servidores na VLAN 20, gerência dos switches da matriz na VLAN 99, FW-HQ na VLAN de trânsito,
# SW-CORE com uma SVI por VLAN
INV_ETAPAA = {ip: v for ip, v in INV_ETAPA0.items()
              if ip not in ('10.10.10.21', '10.10.10.22', '10.10.10.1', '10.10.10.2', '10.10.10.3', '10.10.10.4')}
INV_ETAPAA.update({
    '10.10.20.21': ('APLICACAO', 'servidor'), '10.10.20.22': ('ARQUIVOS', 'servidor'),
    '10.10.100.1': ('FW-HQ', 'firewall'),
    '10.10.10.1': ('SW-CORE', 'switch'), '10.10.20.1': ('SW-CORE', 'switch'), '10.10.99.1': ('SW-CORE', 'switch'),
    '10.10.100.2': ('SW-CORE', 'switch'), '10.10.99.3': ('SW-ACC1', 'switch'), '10.10.99.4': ('SW-ACC2', 'switch'),
})
# etapa B1 (e B2): o gateway da VLAN 20 passa do SW-CORE para o FW-HQ (enclave)
INV_ETAPAB = dict(INV_ETAPAA)
INV_ETAPAB['10.10.20.1'] = ('FW-HQ', 'firewall')
INVENTARIOS = {'0': INV_ETAPA0, 'A': INV_ETAPAA, 'B1': INV_ETAPAB, 'B2': INV_ETAPAB}
INV = INVENTARIOS.get(A.etapa.split('-')[0], INV_ETAPA0)
GERENCIA = {22, 23, 80, 443}          # portas de gerência quando o destino é equipamento de rede
REDE = {'firewall', 'roteador', 'switch'}

p = g.Projeto(A.projeto)
nos = {n['name']: n for n in g.api('GET', f'/projects/{p.id}/nodes')}


def nmap(origem, args, arq, t=3600):
    c = g.conteiner(p, nos[origem])
    # memória de ARP limpa: um nó substituído (MAC novo) apareceria como inalcançável até a entrada expirar
    g.vm(f'docker exec {c} ip neigh flush all')
    alvos = ' '.join(ip for ip, (eq, _) in INV.items() if eq != origem)
    g.vm(f'docker exec {c} sh -c "nmap {args} -oX /tmp/{arq} {alvos} >/dev/null 2>&1"', t)
    xml = g.vm(f'docker exec {c} cat /tmp/{arq}', 120)
    (SAIDA / f'{origem}_{arq}').write_text(xml, encoding='utf-8')
    return ET.fromstring(xml[xml.find('<?xml'):] if '<?xml' in xml else xml)


def hosts(raiz):
    for h in raiz.iter('host'):
        ip = next(a.get('addr') for a in h.iter('address') if a.get('addrtype') == 'ipv4')
        yield ip, h


# ---------------------------------------------------------------- varreduras
alcance, servicos = {}, []
if A.reanalisar:
    with open(SAIDA / 'alcance.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            r['servicos_abertos'] = int(r['servicos_abertos']); alcance[(r['origem'], r['ip'])] = r
    with open(SAIDA / 'servicos.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            r['porta'] = int(r['porta']); servicos.append(r)
    A.origens = list(dict.fromkeys(r['origem'] for r in alcance.values()))
for org in ([] if A.reanalisar else A.origens):
    t0 = time.time()
    r = nmap(org, '-n -sn --disable-arp-ping -PE -PS21,22,23,80,139,443,445,3389 -PA80 --reason', 'descoberta.xml', 900)
    up = {ip for ip, h in hosts(r) if h.find('status').get('state') == 'up'}
    log(f'{org}: alcance de rede {len(up)}/{len(INV) - 1} em {time.time() - t0:.0f} s')
    t0 = time.time()
    r = nmap(org, '-n -Pn -sS -sV -T4 --top-ports 1000 --exclude-ports 5201 --max-retries 2 --host-timeout 20m --open',
             'servicos.xml', 7200)
    for ip, h in hosts(r):
        for pt in h.iter('port'):
            if pt.find('state').get('state') != 'open':
                continue
            s = pt.find('service'); s = s if s is not None else ET.Element('service')
            cpes = [c.text for c in s.findall('cpe')]
            eq, cl = INV[ip]
            servicos.append(dict(etapa=A.etapa, origem=org, ip=ip, equipamento=eq, classe=cl, porta=int(pt.get('portid')),
                                 protocolo=pt.get('protocol'), servico=s.get('name', ''), produto=s.get('product', ''),
                                 versao=s.get('version', ''), cpe=' '.join(cpes)))
    for ip, (eq, cl) in INV.items():
        if eq == org:
            continue
        n = sum(1 for s in servicos if s['origem'] == org and s['ip'] == ip)
        # alcançável = respondeu à descoberta OU tem serviço aberto na varredura de portas
        alcance[(org, ip)] = dict(etapa=A.etapa, origem=org, ip=ip, equipamento=eq, classe=cl,
                                  alcance_rede='sim' if (ip in up or n > 0) else 'nao', servicos_abertos=n)
    log(f'{org}: {sum(1 for s in servicos if s["origem"] == org)} serviços abertos em {time.time() - t0:.0f} s')

# ---------------------------------------------------------------- portal cativo (etapas B)
# Para quem não fez login, o portal do FW-HQ responde às conexões web (80/443) de QUALQUER destino, redirecionando
# para a página de login: o Nmap vê "80/tcp open http OPNsense" em servidores, roteadores e PCs que nem alcança.
# No próprio FW-HQ, as portas 443 e 9000 também são o portal (respondem em HTTP simples, sem TLS).
# Um serviço cuja resposta, em HTTP ou HTTPS, é esse redirecionamento é marcado como interceptado e sai da contagem;
# a página de login (8000) responde 200 e continua contada, como serviço real do firewall.
def interceptado(org, ip, porta):
    try:
        c = g.conteiner(p, nos[org])
    except Exception:
        return False
    for esquema in ('http', 'https'):
        try:
            r = g.vm(f"docker exec {c} curl -sk -m 6 -o /dev/null -w '%{{redirect_url}}' {esquema}://{ip}:{porta}/", 30)
        except Exception:
            continue
        if ':8000/index.html' in r or 'captiveportal' in r:
            return True
    return False


for s in servicos:
    if s.get('interceptado_portal') == 'sim':
        continue                                           # --reanalisar: já confirmado antes
    s['interceptado_portal'] = 'sim' if interceptado(s['origem'], s['ip'], int(s['porta'])) else 'nao'
reais = [s for s in servicos if s['interceptado_portal'] == 'nao']
# alcance: o motivo da descoberta "syn-ack" pode ser o próprio portal; só conta se houver serviço real
motivo = {}
for org in A.origens:
    arq = SAIDA / f'{org}_descoberta.xml'
    if arq.exists():
        x = arq.read_text(encoding='utf-8')
        for ip, h in hosts(ET.fromstring(x[x.find('<?xml'):] if '<?xml' in x else x)):
            st = h.find('status')
            if st.get('state') == 'up':
                motivo[(org, ip)] = st.get('reason')
for (org, ip), a in alcance.items():
    n = sum(1 for s in reais if s['origem'] == org and s['ip'] == ip)
    m = motivo.get((org, ip), '')
    a['servicos_abertos'] = n
    a['motivo_descoberta'] = m
    a['alcance_rede'] = 'sim' if (n > 0 or (m and m != 'syn-ack')) else 'nao'
n_int = sum(1 for s in servicos if s['interceptado_portal'] == 'sim')
if n_int:
    log(f'{n_int} serviço(s) web interceptado(s) pelo portal cativo (fora da contagem)')

# ---------------------------------------------------------------- vulnerabilidades (vulners, no Windows)
cache = json.loads(CACHE.read_text(encoding='utf-8')) if CACHE.exists() else {}


def versao_completa(cpe):
    """Versão com ao menos 'maior.menor' (ex.: 1.25.1). 'samba:4' não serve: casaria com todas as CVEs da família 4.x."""
    partes = cpe.split(':')
    v = partes[4] if len(partes) > 4 else ''
    return v if '.' in v else ''


def consultar(cpe):
    """CVEs (id, cvss) de um CPE com versão completa, pela API pública do vulners (a mesma do vulners.nse)."""
    versao = versao_completa(cpe)
    if not versao:
        return []
    if cpe in cache:
        return cache[cpe]
    url = ('https://vulners.com/api/v3/burp/software/?' +
           urllib.parse.urlencode({'software': cpe, 'version': versao, 'type': 'cpe'}))
    try:
        d = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Vulners NMAP Plugin 1.7'}), timeout=30).read())
    except Exception as e:
        log('vulners falhou para', cpe, e); return None
    cves = []
    for it in (d.get('data') or {}).get('search', []):
        s = it.get('_source', {})
        if s.get('type') != 'cve':
            continue
        nota = ((s.get('cvss3') or {}).get('cvssV3') or {}).get('baseScore') or (s.get('cvss') or {}).get('score') or 0
        cves.append([s.get('id'), float(nota)])
    cache[cpe] = cves
    time.sleep(1)
    return cves


def severidade(n):
    return 'critica' if n >= 9 else 'alta' if n >= 7 else 'media' if n >= 4 else 'baixa' if n > 0 else 'sem nota'


vulns = []
for cpe in sorted({c for s in reais for c in s['cpe'].split() if c}):
    for cve, nota in (consultar(cpe) or []):
        vulns.append(dict(cpe=cpe, cve=cve, cvss=nota, severidade=severidade(nota)))
CACHE.write_text(json.dumps(cache, indent=1), encoding='utf-8')
por_cpe = defaultdict(list)
for v in vulns:
    por_cpe[v['cpe']].append(v)

# ---------------------------------------------------------------- gravação e resumo
def gravar(nome, linhas, campos):
    with open(SAIDA / nome, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, campos); w.writeheader(); w.writerows(linhas)

gravar('alcance.csv', list(alcance.values()), ['etapa', 'origem', 'ip', 'equipamento', 'classe', 'alcance_rede', 'servicos_abertos', 'motivo_descoberta'])
gravar('servicos.csv', servicos, ['etapa', 'origem', 'ip', 'equipamento', 'classe', 'porta', 'protocolo', 'servico', 'produto', 'versao', 'cpe', 'interceptado_portal'])
gravar('vulnerabilidades.csv', vulns, ['cpe', 'cve', 'cvss', 'severidade'])

resumo = {}
md = [f'# Segurança — etapa {A.etapa} ({A.projeto})', '']
for org in A.origens:
    al = [a for a in alcance.values() if a['origem'] == org]
    sv = [s for s in reais if s['origem'] == org]
    exp = defaultdict(int); cves_unicas = set()
    eq_cve = {}                      # (equipamento, cve) -> severidade: cada falha conta uma vez por equipamento
    for s in sv:
        for c in s['cpe'].split():
            for v in por_cpe.get(c, []):
                exp[v['severidade']] += 1; cves_unicas.add(v['cve'])
                eq_cve[(s['equipamento'], v['cve'])] = v['severidade']
    eq_sev = defaultdict(int)
    for sev in eq_cve.values():
        eq_sev[sev] += 1
    eq_serv = {(s['equipamento'], s['porta']) for s in sv}   # serviço contado uma vez por equipamento
    eqs = lambda f: sorted({a['equipamento'] for a in al if f(a)})
    r = {
        'equipamentos_no_inventario': len({a['equipamento'] for a in al}),
        'servicos_por_equipamento': len(eq_serv),
        'servicos_de_gerencia_por_equipamento': sum(1 for e, pt in eq_serv
                                                   if pt in GERENCIA and next(s['classe'] for s in sv if s['equipamento'] == e) in REDE),
        'vulnerabilidades_por_equipamento_total': len(eq_cve),
        'vulnerabilidades_por_equipamento_por_severidade': dict(eq_sev),
        'destinos_no_inventario': len(al),
        'enderecos_alcancaveis': sum(a['alcance_rede'] == 'sim' for a in al),
        'equipamentos_alcancaveis': eqs(lambda a: a['alcance_rede'] == 'sim'),
        'enderecos_com_servico': sum(a['servicos_abertos'] > 0 for a in al),
        'equipamentos_com_servico': eqs(lambda a: a['servicos_abertos'] > 0),
        'servicos_abertos': len(sv),
        'servicos_por_classe': {cl: sum(s['classe'] == cl for s in sv) for cl in ['servidor', 'estacao', 'firewall', 'roteador', 'switch']},
        'servicos_de_gerencia_em_equipamentos_de_rede': sum(s['classe'] in REDE and s['porta'] in GERENCIA for s in sv),
        'servidores_alcancaveis_com_servico': eqs(lambda a: a['classe'] == 'servidor' and a['servicos_abertos'] > 0),
        'vulnerabilidades_expostas_por_severidade': dict(exp),
        'vulnerabilidades_expostas_total': sum(exp.values()),
        'cves_unicas_expostas': len(cves_unicas),
        'servicos_sem_versao_completa': sum(1 for s in sv if not any(versao_completa(c) for c in s['cpe'].split())),
    }
    resumo[org] = r
    md += [f'## Origem: {org}', '',
           '**Por equipamento (métrica principal):**', '',
           f"- Equipamentos alcançáveis: **{len(r['equipamentos_alcancaveis'])}/{r['equipamentos_no_inventario']}**; com serviço aberto: **{len(r['equipamentos_com_servico'])}**",
           f"- Serviços expostos: **{r['servicos_por_equipamento']}** (de gerência em equipamentos de rede: **{r['servicos_de_gerencia_por_equipamento']}**)",
           f"- Vulnerabilidades expostas (equipamento × CVE): **{r['vulnerabilidades_por_equipamento_total']}** {r['vulnerabilidades_por_equipamento_por_severidade']}",
           '', '**Por endereço (caminhos de exposição):**', '',
           f"- Endereços alcançáveis: **{r['enderecos_alcancaveis']}/{r['destinos_no_inventario']}** ({len(r['equipamentos_alcancaveis'])} equipamentos)",
           f"- Endereços com serviço aberto: **{r['enderecos_com_servico']}**; serviços abertos: **{r['servicos_abertos']}** {r['servicos_por_classe']}",
           f"- Serviços de gerência expostos em equipamentos de rede: **{r['servicos_de_gerencia_em_equipamentos_de_rede']}**",
           f"- Servidores alcançáveis com serviço: {', '.join(r['servidores_alcancaveis_com_servico']) or 'nenhum'}",
           f"- Vulnerabilidades expostas (serviço × CVE): **{r['vulnerabilidades_expostas_total']}** {r['vulnerabilidades_expostas_por_severidade']}; CVEs únicas: {r['cves_unicas_expostas']}",
           f"- Serviços sem versão completa identificada (fora da contagem de CVEs): {r['servicos_sem_versao_completa']}", '']
md += ['## Produtos encontrados e CVEs conhecidas', '', '| CPE | CVEs | críticas | altas | médias | baixas |', '|---|---|---|---|---|---|']
for cpe in sorted({c for s in reais for c in s['cpe'].split() if c}):
    vs = por_cpe.get(cpe, [])
    cnt = lambda sv: sum(v['severidade'] == sv for v in vs)
    md.append(f"| {cpe} | {len(vs) if versao_completa(cpe) else 'sem versão completa'} | {cnt('critica')} | {cnt('alta')} | {cnt('media')} | {cnt('baixa')} |")
(SAIDA / 'resumo.json').write_text(json.dumps({'etapa': A.etapa, 'projeto': A.projeto, 'origens': resumo}, indent=1, ensure_ascii=False), encoding='utf-8')
(SAIDA / 'resumo.md').write_text('\n'.join(md), encoding='utf-8')
print('\n'.join(md))
