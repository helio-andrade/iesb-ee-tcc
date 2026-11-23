"""Etapa B2: a B1 mais túneis IPsec (IKEv2) em estrela entre os firewalls.

Uso: python montar_etapaB2.py [passos...]      (padrão: todos; idempotente)
Passos: provedor, wan, tuneis, ativar, regras, mss, teste, backup

Projeto TCC-etapa-B2 (duplicado de TCC-etapa-B1-navegador, que já traz a correção do DHCP da VLAN 10).
Os PCs de navegador ficam DESLIGADOS (fora das medições).

Túneis (policy-based, swanctl):
  FW-HQ <-> FW-F1: 10.10.0.0/16 + 10.30.0.0/16  <->  10.20.0.0/16
  FW-HQ <-> FW-F2: 10.10.0.0/16 + 10.20.0.0/16  <->  10.30.0.0/16
  -> o tráfego filial <-> filial passa pela matriz (estrela). RTT emulado igual ao direto: 20 + 60 = 80 ms.
Criptografia (NIST SP 800-77 Rev. 1): IKE aes256gcm16-sha256-ecp256 (AES-256-GCM, PRF SHA-256, grupo 19);
ESP aes256gcm16-ecp256 (AES-256-GCM com PFS no grupo 19). Autenticação por chave pré-compartilhada (limitação: o ideal
seria certificado). MSS 1400 (campo da interface = 1440) nas LANs das filiais (todo tráfego entre unidades passa por uma delas): ESP com AES-GCM em
modo túnel = IP 20 + ESP 8 + IV 8 + trailer 2-5 + ICV 16 -> pacote interno de 1440 cabe em 1500 (MSS 1440 - 40).
As regras de medição saem da WAN (texto claro) e vão para a interface IPsec: entre unidades, só tráfego cifrado.
"""
import json, pathlib, secrets, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import gns3lab as g

def log(*a): print(time.strftime('%H:%M:%S'), *a, flush=True)

RAIZ = pathlib.Path(__file__).resolve().parents[1]
ET = RAIZ / 'etapa-B2'; ET.mkdir(exist_ok=True)
CHAVES = json.loads((RAIZ / 'dados' / 'opnsense_api_keys.json').read_text())
p = g.Projeto('TCC-etapa-B2')
N = {n['name']: n for n in g.api('GET', f'/projects/{p.id}/nodes')}
FW = {fw: g.OpnAPIGer(CHAVES[f'etapa0-{fw}']) for fw in ('FW-HQ', 'FW-F1', 'FW-F2')}
WAN = {'FW-HQ': '10.255.1.2', 'FW-F1': '10.255.2.2', 'FW-F2': '10.255.3.2'}
REDE = {'FW-HQ': '10.10.0.0/16', 'FW-F1': '10.20.0.0/16', 'FW-F2': '10.30.0.0/16'}
IKE, ESP = 'aes256gcm16-sha256-ecp256', 'aes256gcm16-ecp256'
MSS = '1440'   # campo MSS da interface no OPNsense = valor - 40 no pf (IPv4): 1440 -> max-mss 1400
IP = {'PC-USUARIO': '10.10.10.11', 'HOST-INVADIDO': '10.10.10.12', 'APLICACAO': '10.10.20.21', 'ARQUIVOS': '10.10.20.22',
      'PC-FIL1': '10.20.10.11', 'PC-FIL2': '10.30.10.11'}
# túnel: (firewall da matriz, filial, seletores locais da matriz, seletores locais da filial)
TUNEIS = [('FW-HQ', 'FW-F1', [REDE['FW-HQ'], REDE['FW-F2']], [REDE['FW-F1']]),
          ('FW-HQ', 'FW-F2', [REDE['FW-HQ'], REDE['FW-F1']], [REDE['FW-F2']])]
ARQ_PSK = RAIZ / 'dados' / 'ipsec_psk.json'


def ok(r, oque):
    assert isinstance(r, dict) and r.get('result') in ('saved', 'ok'), f'{oque}: {r}'
    return r.get('uuid')


def regra(api, interface, proto, origem, destino, porta, descr, prefixo='Etapa B2: '):
    return ok(api('POST', 'firewall/filter/add_rule', {'rule': {
        'enabled': '1', 'action': 'pass', 'quick': '1', 'direction': 'in', 'ipprotocol': 'inet', 'protocol': proto,
        'interface': interface, 'source_net': origem, 'destination_net': destino, 'destination_port': porta,
        'description': prefixo + descr}}), descr)


def tem_regra(api, trecho):
    return any(trecho in (r.get('description') or '') for r in api('GET', 'firewall/filter/search_rule').get('rows', []))


def shell_fw(fw, cmd, t=120, arquivo=None):
    con = g.Console(p, N[fw]); assert g.opn_entrar_shell(con)
    if arquivo:
        g.opn_enviar_arquivo(con, arquivo, '/tmp/b2.php')
    out = g.opn_shell(con, cmd, t)
    con.enviar('exit'); return out


# ------------------------------------------------------------------ passos
def passo_provedor():
    """O PROVEDOR só tem rotas entre as unidades e os perfis de enlace (tc/netem) depois de /etc/network/provedor.sh,
    que não roda sozinho quando o nó liga (o ensaio.py reaplica, mas a montagem e os testes precisam antes)."""
    pv = g.conteiner(p, N['PROVEDOR'])
    if '10.255.2.0/30' in g.vm(f'docker exec {pv} ip route', 30) and 'netem' in g.vm(f'docker exec {pv} tc qdisc show dev eth1', 30):
        log('PROVEDOR: rotas e perfis de enlace já aplicados'); return
    log('PROVEDOR: aplicando rotas e perfis de enlace ->', g.vm(f'docker exec {pv} sh /etc/network/provedor.sh', 60).strip()[-20:])


def passo_wan():
    """IKE (UDP 500/4500) e ESP só entre os IPs WAN dos firewalls que formam túnel."""
    pares = {'FW-HQ': ['FW-F1', 'FW-F2'], 'FW-F1': ['FW-HQ'], 'FW-F2': ['FW-HQ']}
    for fw, pares_fw in pares.items():
        api = FW[fw]
        for par in pares_fw:
            d = f'IKE/ESP de {par}'
            if tem_regra(api, d):
                continue
            regra(api, 'wan', 'UDP', WAN[par], WAN[fw], '500', d + ' (IKE)')
            regra(api, 'wan', 'UDP', WAN[par], WAN[fw], '4500', d + ' (NAT-T)')
            regra(api, 'wan', 'ESP', WAN[par], WAN[fw], '', d + ' (ESP)')
        api('POST', 'firewall/filter/apply', {})
    log('WAN: IKE e ESP liberados só entre os firewalls pares')


def psk():
    if ARQ_PSK.exists():
        return json.loads(ARQ_PSK.read_text())
    d = {f'{a}-{b}': secrets.token_urlsafe(30) for a, b, _, _ in TUNEIS}
    ARQ_PSK.write_text(json.dumps(d, indent=1)); return d


def conexao(api, local, remoto, local_ts, remote_ts, chave):
    desc = f'B2: {local} <-> {remoto}'
    if any(r.get('description') == desc for r in api('POST', 'ipsec/connections/search_connection', {}).get('rows', [])):
        return False
    c = ok(api('POST', 'ipsec/connections/add_connection', {'connection': {
        'enabled': '1', 'proposals': IKE, 'version': '2', 'local_addrs': WAN[local], 'remote_addrs': WAN[remoto],
        'mobike': '0', 'unique': 'replace', 'dpd_delay': '10', 'description': desc}}), 'conexão ' + desc)
    ok(api('POST', 'ipsec/connections/add_local', {'local': {'enabled': '1', 'connection': c, 'auth': 'psk', 'id': WAN[local],
                                                             'description': desc + ' (local)'}}), 'local')
    ok(api('POST', 'ipsec/connections/add_remote', {'remote': {'enabled': '1', 'connection': c, 'auth': 'psk', 'id': WAN[remoto],
                                                               'description': desc + ' (remoto)'}}), 'remoto')
    ok(api('POST', 'ipsec/connections/add_child', {'child': {
        'enabled': '1', 'connection': c, 'mode': 'tunnel', 'esp_proposals': ESP, 'start_action': 'trap|start',
        'dpd_action': 'start', 'close_action': 'none', 'local_ts': ','.join(local_ts), 'remote_ts': ','.join(remote_ts),
        'description': desc}}), 'child')
    if not any(r.get('remote_ident') == WAN[remoto] for r in api('POST', 'ipsec/pre_shared_keys/search_item', {}).get('rows', [])):
        ok(api('POST', 'ipsec/pre_shared_keys/add_item', {'preSharedKey': {
            'ident': WAN[local], 'remote_ident': WAN[remoto], 'keyType': 'PSK', 'Key': chave, 'description': desc}}), 'psk')
    return True


def passo_tuneis():
    chaves = psk()
    for hq, fil, ts_hq, ts_fil in TUNEIS:
        k = chaves[f'{hq}-{fil}']
        a = conexao(FW[hq], hq, fil, ts_hq, ts_fil, k)
        b = conexao(FW[fil], fil, hq, ts_fil, ts_hq, k)
        log(f'túnel {hq} <-> {fil}:', 'criado' if a or b else 'já existia', f'| {ts_hq} <-> {ts_fil}')
    # confere a versão gravada (o campo é uma lista de opções)
    c = FW['FW-HQ']('POST', 'ipsec/connections/search_connection', {})['rows'][0]
    det = FW['FW-HQ']('GET', f"ipsec/connections/get_connection/{c['uuid']}")['connection']['version']
    sel = [o['value'] for o in (det if isinstance(det, list) else det.values()) if o.get('selected')]
    log('versão IKE gravada:', sel)
    assert sel == ['IKEv2'], sel


def passo_ativar():
    for fw, api in FW.items():
        # o "Enable" da página de conexões; ipsec/settings/set com general.enabled não liga o serviço
        assert api('POST', 'ipsec/connections/toggle/1', {}).get('status') == 'ok', fw
        assert api('GET', 'ipsec/connections/is_enabled').get('enabled'), fw
        api('POST', 'ipsec/service/reconfigure', {})
    time.sleep(15)
    for fw, api in FW.items():
        f1 = api('POST', 'ipsec/sessions/search_phase1', {}).get('rows', [])
        log(f'{fw}: IPsec', api('GET', 'ipsec/service/status').get('status'), '| fases 1:',
            [(r.get('description') or r.get('name'), r.get('connected')) for r in f1])


def iface_ipsec(api):
    for v in api('GET', 'firewall/filter/get_interface_list').values():
        for i in v.get('items', []):
            if i['value'] == 'enc0' or 'ipsec' in i['label'].lower():
                return i['value']
    raise RuntimeError('interface IPsec não encontrada (IPsec ativo?)')


def passo_regras():
    hq, f1, f2 = FW['FW-HQ'], FW['FW-F1'], FW['FW-F2']
    u, pf1, pf2 = IP['PC-USUARIO'], IP['PC-FIL1'], IP['PC-FIL2']
    novas = [  # (api, origem, destino, descrição) -> TCP/UDP 5201 e ICMP, na interface IPsec
        (f1, u, pf1, 'matriz -> PC-FIL1 pelo túnel'),
        (f2, u, pf2, 'matriz -> PC-FIL2 pelo túnel'),
        (f2, pf1, pf2, 'PC-FIL1 -> PC-FIL2 pelo túnel (via matriz)'),
        (hq, pf1, pf2, 'trânsito PC-FIL1 -> PC-FIL2 (estrela)')]
    for api, o, d, desc in novas:
        if tem_regra(api, desc):
            continue
        ifc = iface_ipsec(api)
        regra(api, ifc, 'TCP/UDP', o, d, '5201', desc + ' (medição)')
        regra(api, ifc, 'ICMP', o, d, '', desc + ' (latência)')
    # a WAN deixa de aceitar os fluxos de medição em texto claro
    n = f1.apagar_regras('matriz -> PC-FIL1 (') + f2.apagar_regras('matriz e filial 1 -> PC-FIL2 (')
    for api in (hq, f1, f2):
        api('POST', 'firewall/filter/apply', {})
    log(f'regras na interface IPsec criadas; {n} regra(s) de medição em texto claro removidas da WAN')


PHP_MSS = r'''<?php
require_once '/usr/local/opnsense/mvc/script/load_phalcon.php';
$cfg = OPNsense\Core\Config::getInstance(); $o = $cfg->object();
$o->interfaces->lan->mss = '%MSS%';
$cfg->save(); echo "MSS_OK\n";
'''.replace('%MSS%', MSS)


def passo_mss():
    for fw in ('FW-F1', 'FW-F2'):
        out = shell_fw(fw, 'php /tmp/b2.php; rm -f /tmp/b2.php; configctl interface reconfigure lan >/dev/null; '
                           'configctl filter reload >/dev/null; sleep 2; pfctl -sa 2>/dev/null | grep "inet all max-mss"',
                       180, arquivo=PHP_MSS)
        log(f'{fw}: campo MSS {MSS} na LAN ->', out.strip().splitlines()[-2:] if out.strip() else '?')


def passo_teste():
    co = {h: g.conteiner(p, N[h]) for h in IP}
    for h in ('APLICACAO', 'PC-FIL1', 'PC-FIL2'):
        g.vm(f'docker exec {co[h]} sh -c "killall iperf3 2>/dev/null; iperf3 -s -D"')
    url = 'http://10.10.100.1:8000/api/captiveportal/access/logon/0'
    g.vm(f"docker exec {co['PC-USUARIO']} curl -s -m 15 -X POST -d 'user=usuario1&password=Senha.Tcc1' {url}")
    def ping(o, d): return ' 0% packet loss' in g.vm(f"docker exec {co[o]} ping -c 3 -W 2 {IP[d] if d in IP else d} | grep loss")
    for _ in range(12):                              # espera os túneis (o tráfego dispara a negociação: start_action trap)
        if ping('PC-USUARIO', 'PC-FIL1') and ping('PC-USUARIO', 'PC-FIL2') and ping('PC-FIL1', 'PC-FIL2'):
            break
        time.sleep(10)
    def web(o, d): return 'Aplicacao interna' in g.vm(f"docker exec {co[o]} curl -s -m 6 http://{IP[d]}/")
    def tcp(o, d, pt): return 'ABERTO' in g.vm(f"docker exec {co[o]} sh -c 'nc -z -w 3 {IP[d] if d in IP else d} {pt} && echo ABERTO'")
    casos = [
        ('PC-USUARIO -> APLICACAO (ping)', lambda: ping('PC-USUARIO', 'APLICACAO'), True),
        ('PC-USUARIO -> APLICACAO (página web)', lambda: web('PC-USUARIO', 'APLICACAO'), True),
        ('PC-USUARIO -> ARQUIVOS :445', lambda: tcp('PC-USUARIO', 'ARQUIVOS', 445), True),
        ('PC-USUARIO -> PC-FIL1 (ping, túnel)', lambda: ping('PC-USUARIO', 'PC-FIL1'), True),
        ('PC-USUARIO -> PC-FIL2 (ping, túnel)', lambda: ping('PC-USUARIO', 'PC-FIL2'), True),
        ('PC-USUARIO -> PC-FIL1 :5201 (túnel)', lambda: tcp('PC-USUARIO', 'PC-FIL1', 5201), True),
        ('PC-FIL1 -> PC-FIL2 (ping, túnel via matriz)', lambda: ping('PC-FIL1', 'PC-FIL2'), True),
        ('PC-FIL1 -> PC-FIL2 :5201 (túnel via matriz)', lambda: tcp('PC-FIL1', 'PC-FIL2', 5201), True),
        ('PC-USUARIO -> ARQUIVOS :22 (SSH)', lambda: tcp('PC-USUARIO', 'ARQUIVOS', 22), False),
        ('PC-USUARIO -> SW-ACC1 10.10.99.3 (ping)', lambda: ping('PC-USUARIO', '10.10.99.3'), False),
        ('HOST-INVADIDO (sem login) -> APLICACAO (página web)', lambda: web('HOST-INVADIDO', 'APLICACAO'), False),
        ('HOST-INVADIDO (sem login) -> APLICACAO :443', lambda: tcp('HOST-INVADIDO', 'APLICACAO', 443), False),
        ('HOST-INVADIDO -> ARQUIVOS :445', lambda: tcp('HOST-INVADIDO', 'ARQUIVOS', 445), False),
        ('HOST-INVADIDO -> R-HQ 10.255.1.1 :23', lambda: tcp('HOST-INVADIDO', '10.255.1.1', 23), False),
        ('PC-FIL1 -> APLICACAO (página web)', lambda: web('PC-FIL1', 'APLICACAO'), False),
        ('PC-FIL1 -> R-FIL1 10.255.2.1 :22', lambda: tcp('PC-FIL1', '10.255.2.1', 22), False),
        ('PC-FIL1 -> PC-USUARIO (ping)', lambda: ping('PC-FIL1', 'PC-USUARIO'), False),
        ('PC-FIL2 -> PC-FIL1 (ping)', lambda: ping('PC-FIL2', 'PC-FIL1'), False),
        ('APLICACAO -> PC-USUARIO (ping, servidor não inicia fluxos)', lambda: ping('APLICACAO', 'PC-USUARIO'), False),
        ('HOST-INVADIDO -> PC-USUARIO (ping, mesma VLAN: limitação)', lambda: ping('HOST-INVADIDO', 'PC-USUARIO'), True),
    ]
    linhas, falhas = [], 0
    for desc, f, esperado in casos:
        r = f(); certo = r == esperado; falhas += not certo
        linhas.append(f"{'OK ' if certo else 'ERRO'} {desc}: {'passa' if r else 'bloqueado'} (esperado: {'passa' if esperado else 'bloqueado'})")
        log(linhas[-1])
    # evidências do túnel: caminho filial -> filial e o que o provedor enxerga
    tr = g.vm(f"docker exec {co['PC-FIL1']} traceroute -I -n -w 2 -q 1 {IP['PC-FIL2']}", 60).strip()
    prov = g.conteiner(p, N['PROVEDOR'])
    g.vm(f"docker exec -d {co['PC-USUARIO']} ping -c 6 -i 0.5 {IP['PC-FIL1']}")
    cap = g.vm(f"docker exec {prov} sh -c 'timeout 5 tcpdump -n -i any -c 12 \"esp or icmp\" 2>/dev/null || echo SEM_TCPDUMP'", 30)
    esp, icmp = cap.count(' ESP('), sum(1 for l in cap.splitlines() if 'ICMP' in l and ('10.10.' in l or '10.20.' in l))
    sa = [l.rstrip() for l in shell_fw('FW-HQ', 'swanctl --list-sas 2>/dev/null', 60).splitlines()
          if any(k in l for k in ('ESTABLISHED', 'INSTALLED', 'AES', ' in ', ' out ', 'local  1', 'remote 1'))]
    extra = ['', 'traceroute PC-FIL1 -> PC-FIL2:', tr, '',
             f'captura no PROVEDOR (ping matriz -> filial 1): {esp} pacotes ESP, {icmp} ICMP em texto claro entre as unidades'
             + (' (tcpdump indisponível)' if 'SEM_TCPDUMP' in cap else ''), '', 'SAs (fase 2):'] + sa
    (ET / 'teste_funcional.txt').write_text('\n'.join(linhas + extra) + '\n', encoding='utf-8')
    log(f'teste funcional: {len(casos) - falhas}/{len(casos)} conforme a política')
    log('\n'.join(extra))


def passo_backup():
    for fw, api in FW.items():
        api.backup(ET / f'{fw}.xml')
    for nome in ('R-HQ', 'R-FIL1', 'R-FIL2', 'SW-CORE', 'SW-ACC1', 'SW-ACC2', 'SW-FIL1', 'SW-FIL2'):
        con = g.Console(p, N[nome]); g.cisco_pronto(con, 60)
        run = g.cisco_show(con, 'show running-config', 8)
        (ET / f'{nome}.cfg').write_text(run[run.find('Building configuration'):] if 'Building configuration' in run else run, encoding='utf-8')
    log('backups em lab/etapa-B2/')


PASSOS = ['provedor', 'wan', 'tuneis', 'ativar', 'regras', 'mss', 'teste', 'backup']
if __name__ == '__main__':
    for nome in (sys.argv[1:] or PASSOS):
        log('==', nome); globals()['passo_' + nome]()
