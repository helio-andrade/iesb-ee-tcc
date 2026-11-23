"""Cópia da etapa B1 com um PC de navegador (webterm: Firefox + terminal, console VNC) na matriz e em cada filial.

Uso: python navegadores_b1.py [passos...]     (padrão: todos; o script é idempotente)
Passos: duplicar, nos, ligar, l2, firewall, rotulos, teste, backup

- O projeto original TCC-etapa-B1 NÃO é alterado (é a base da etapa B2): ele é fechado e duplicado para
  TCC-etapa-B1-navegador, onde os PCs são acrescentados. Só um dos dois pode ficar ligado por vez (mesmos IPs de gerência).
- Os PCs servem a testes visuais (portal cativo, aplicação web) e ficam fora das medições: não entram no inventário de
  segurança nem nas baterias de ensaio.
- PC-NAV-HQ (VLAN 10 da matriz) recebe as mesmas liberações de negócio do PC-USUARIO (HTTP/HTTPS e ICMP na aplicação,
  SMB nos arquivos), sempre depois do login no portal. Os das filiais seguem a política da B1 (sem acesso ao enclave).
- Imagem gns3/webterm (Debian 12, Firefox ESR, JWM, LXTerminal: botão direito na área de trabalho -> Terminal).
"""
import base64, json, pathlib, sys, time
from xml.sax.saxutils import escape
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import gns3lab as g

def log(*a): print(time.strftime('%H:%M:%S'), *a, flush=True)

ORIGEM, DESTINO = 'TCC-etapa-B1', 'TCC-etapa-B1-navegador'
RAIZ = pathlib.Path(__file__).resolve().parents[1]
PASTA = RAIZ / 'etapa-B1-navegador'; PASTA.mkdir(exist_ok=True)
CHAVES = json.loads((RAIZ / 'dados' / 'opnsense_api_keys.json').read_text())
TEMPLATE = 'TCC - Navegador'
IMAGEM = 'gns3/webterm:latest'
# nome: (switch, porta IOL (adaptador, porta), VLAN, IP, gateway, posição)
PCS = {'PC-NAV-HQ': ('SW-ACC1', (0, 3), '10', '10.10.10.13', '10.10.10.1', (-990, 283)),
       'PC-NAV-F1': ('SW-FIL1', (0, 2), '1', '10.20.10.13', '10.20.10.1', (180, 300)),
       'PC-NAV-F2': ('SW-FIL2', (0, 2), '1', '10.30.10.13', '10.30.10.1', (490, 220))}
APLICACAO, ARQUIVOS = '10.10.20.21', '10.10.20.22'
PORTAL = 'http://10.10.100.1:8000/api/captiveportal/access'
COR = '#1f3a93'


def projetos():
    return {x['name']: x for x in g.api('GET', '/projects')}


def passo_duplicar():
    ps = projetos()
    if DESTINO in ps:
        log(f'{DESTINO} já existe'); return
    org = ps[ORIGEM]
    # aberto e parado: com o projeto fechado, a duplicação falhou ("hda_disk.qcow2 not found on compute")
    if org['status'] != 'opened':
        g.api('POST', f"/projects/{org['project_id']}/open", {})
    g.api('POST', f"/projects/{org['project_id']}/nodes/stop", {})
    log(f'{ORIGEM} aberto e parado (não é alterado; fica como base da B2)')
    t0 = time.time()
    g.api('POST', f"/projects/{org['project_id']}/duplicate", {'name': DESTINO}, timeout=900)
    log(f'{DESTINO} criado por duplicação em {time.time() - t0:.0f} s')


def proj():
    return g.Projeto(DESTINO)


def nos(p):
    return {n['name']: n for n in g.api('GET', f'/projects/{p.id}/nodes')}


def mac_ios(mac):
    h = mac.replace(':', '').lower()
    return f'{h[0:4]}.{h[4:8]}.{h[8:12]}'


def passo_nos():
    p = proj(); N = nos(p)
    if not any(t['name'] == TEMPLATE for t in g.api('GET', '/templates')):
        g.api('POST', '/templates', {'name': TEMPLATE, 'template_type': 'docker', 'compute_id': 'vm', 'image': IMAGEM,
                                     'adapters': 1, 'console_type': 'vnc', 'console_resolution': '1280x800',
                                     'category': 'guest', 'default_name_format': 'NAV-{0}',
                                     'symbol': ':/symbols/classic/computer.svg'})
        log(f'template "{TEMPLATE}" criado ({IMAGEM}, console VNC)')
    links = g.api('GET', f'/projects/{p.id}/links')
    for nome, (sw, porta, vlan, ip, gw, (x, y)) in PCS.items():
        if nome in N:
            log(nome, 'já existe'); continue
        ocupada = any(e['node_id'] == N[sw]['node_id'] and (e['adapter_number'], e['port_number']) == porta
                      for l in links for e in l['nodes'])
        assert not ocupada, f'{sw} {porta} ocupada'
        n = p.de_template(TEMPLATE, nome, x, y, symbol=':/symbols/classic/computer.svg')
        iface = f'auto eth0\niface eth0 inet static\n\taddress {ip}\n\tnetmask 255.255.255.0\n\tgateway {gw}\n'
        g.api('POST', f"/projects/{p.id}/nodes/{n['node_id']}/files/etc/network/interfaces", bruto=iface)
        p.link(n, (0, 0), N[sw], porta)
        log(f'{nome}: {ip}/24 gw {gw} -> {sw} e{porta[0]}/{porta[1]} (VLAN {vlan})')


def passo_ligar():
    p = proj()
    p.iniciar()
    log('ligando todos os nós...')
    hq = g.OpnAPIGer(CHAVES['etapa0-FW-HQ'])
    for _ in range(60):                                                 # o FW-HQ é o último a ficar pronto
        try:
            hq('GET', 'core/firmware/status'); break
        except Exception:
            time.sleep(10)
    N = nos(p)
    for sw in ('SW-ACC1', 'SW-FIL1', 'SW-FIL2'):
        assert g.cisco_pronto(g.Console(p, N[sw]), 300), sw
    log('firewall da matriz e switches prontos')


def passo_l2():
    p = proj(); N = nos(p)
    for nome, (sw, porta, vlan, ip, gw, _) in PCS.items():
        mac = g.api('GET', f"/projects/{p.id}/nodes/{N[nome]['node_id']}")['properties']['mac_address']
        cfg = [f'arp access-list ARP-HOSTS', f' permit ip host {ip} mac host {mac_ios(mac)}', 'exit',
               f'interface Ethernet{porta[0]}/{porta[1]}', ' switchport mode access',
               f' switchport access vlan {vlan}' if vlan != '1' else '',
               ' switchport port-security', ' switchport port-security maximum 1',
               f' switchport port-security mac-address {mac_ios(mac)}', ' switchport port-security violation restrict',
               ' no shutdown']
        con = g.Console(p, N[sw]); assert g.cisco_pronto(con, 120), sw
        g.cisco_config(con, '\n'.join(l for l in cfg if l), 0.6)
        assert g.cisco_salvar(con), sw
        acl = g.cisco_show(con, 'show arp access-list ARP-HOSTS', 4)
        log(f'{sw}: {nome} ({mac}) no DAI e no port security ->', 'ok' if ip in acl else 'FALHOU: ' + acl[-200:])


def passo_firewall():
    hq = g.OpnAPIGer(CHAVES['etapa0-FW-HQ'])
    if any('PC-NAV-HQ' in (r.get('description') or '') for r in hq('GET', 'firewall/filter/search_rule').get('rows', [])):
        log('regras do PC-NAV-HQ já existem'); return
    ip = PCS['PC-NAV-HQ'][3]
    # o campo de porta aceita uma porta, um intervalo ou um alias, não uma lista ("80,443")
    for proto, dst, porta, descr in (('TCP', APLICACAO, '80', 'aplicação (HTTP)'), ('TCP', APLICACAO, '443', 'aplicação (HTTPS)'),
                                     ('ICMP', APLICACAO, '', 'aplicação (ping)'),
                                     ('TCP', ARQUIVOS, '445', 'arquivos (SMB)')):
        r = hq('POST', 'firewall/filter/add_rule', {'rule': {
            'enabled': '1', 'action': 'pass', 'quick': '1', 'direction': 'in', 'ipprotocol': 'inet', 'protocol': proto,
            'interface': 'lan', 'source_net': ip, 'destination_net': dst, 'destination_port': porta,
            'description': f'B1-navegador: PC-NAV-HQ -> {descr}'}})
        assert r.get('result') == 'saved', r
    hq('POST', 'firewall/filter/apply', {})
    log('FW-HQ: PC-NAV-HQ com os fluxos de negócio do usuário (após o login no portal)')


def passo_dhcp():
    """Corrige o relay DHCP herdado do B1 original: o IOS envia o pedido com origem = giaddr = 10.10.10.1, que nem a regra
    (origem 10.10.100.2) nem a lista de liberados do portal aceitavam. O dnsmasq escolhe a faixa pelo giaddr, então a
    origem tem de continuar 10.10.10.1 (mudar a source-interface do relay no SW-CORE também muda o giaddr e quebra)."""
    hq = g.OpnAPIGer(CHAVES['etapa0-FW-HQ'])
    if not any('relay DHCP da VLAN 10' in (r.get('description') or '') for r in hq('GET', 'firewall/filter/search_rule')['rows']):
        r = hq('POST', 'firewall/filter/add_rule', {'rule': {'enabled': '1', 'action': 'pass', 'quick': '1', 'direction': 'in',
            'ipprotocol': 'inet', 'protocol': 'UDP', 'interface': 'lan', 'source_net': '10.10.10.1', 'destination_net': '10.10.100.1',
            'destination_port': '67', 'description': 'Etapa B1: relay DHCP da VLAN 10 (origem = giaddr 10.10.10.1)'}})
        assert r.get('result') == 'saved', r
        hq('POST', 'firewall/filter/apply', {})
    z = hq('GET', 'captiveportal/settings/search_zones')['rows'][0]
    lib = hq('GET', f"captiveportal/settings/get_zone/{z['uuid']}")['zone'].get('allowedAddresses')
    lib = ','.join(k for k, v in lib.items() if v.get('selected')) if isinstance(lib, dict) else (lib or '')
    if '10.10.10.1' not in lib.split(','):
        hq('POST', f"captiveportal/settings/set_zone/{z['uuid']}", {'zone': {'allowedAddresses': lib + ',10.10.10.1'}})
        hq('POST', 'captiveportal/service/reconfigure', {}); time.sleep(8)
    log('DHCP da VLAN 10: regra do relay (origem 10.10.10.1) e 10.10.10.1 liberado no portal')


def svg_texto(linhas, fs=10):
    w = max(len(l) for l in linhas) * 6.2 + 10; h = len(linhas) * (fs + 4) + 6
    return (f'<svg width="{w:.0f}" height="{h:.0f}"><text font-family="Consolas" font-size="{fs}" fill="{COR}" '
            f'fill-opacity="1.0">{chr(10).join(escape(l) for l in linhas)}</text></svg>')


def passo_rotulos():
    p = proj(); N = nos(p)
    reg = PASTA / 'rotulos.json'
    ids = json.loads(reg.read_text()) if reg.exists() else {}
    existentes = {d['drawing_id'] for d in g.api('GET', f'/projects/{p.id}/drawings')}
    for nome, (sw, porta, vlan, ip, gw, _) in PCS.items():
        linhas = [f'{ip}/24', f'gw {gw}', 'navegador (VNC)']
        n = N[nome]
        if ids.get(nome) in existentes:
            g.api('PUT', f'/projects/{p.id}/drawings/{ids[nome]}', {'svg': svg_texto(linhas)})
        else:
            d = g.api('POST', f'/projects/{p.id}/drawings', {'x': int(n['x'] - 20), 'y': int(n['y'] + 75), 'z': 2, 'svg': svg_texto(linhas)})
            ids[nome] = d['drawing_id']
    reg.write_text(json.dumps(ids))
    log('anotações dos PCs de navegador criadas')


def passo_teste():
    p = proj(); N = nos(p)
    # PCs com DHCP (relay até o FW-HQ) que ligaram antes do firewall ficam sem endereço: reinicia-os
    for n in ('PC-USUARIO', 'HOST-INVADIDO'):
        if 'inet ' not in g.vm(f"docker exec {g.conteiner(p, N[n])} ip -4 -o addr show eth0", 30):
            p.parar(N[n]); p.iniciar(N[n]); log(n, 'sem endereço (DHCP antes do FW-HQ): reiniciado')
    time.sleep(10); N = nos(p)
    c = {n: g.conteiner(p, N[n]) for n in PCS}
    sh = lambda n, cmd: g.vm(f"docker exec {c[n]} sh -c {json.dumps(cmd)}", 60).strip()
    res = []
    def chk(desc, obtido, esperado):
        res.append(f"{'OK ' if obtido == esperado else 'ERRO'} {desc}: {obtido} (esperado: {esperado})")
    ping = lambda n, ip: 'passa' if ' 0% packet loss' in sh(n, f'ping -c 2 -W 2 {ip}') else 'bloqueado'
    http = lambda n, url: {'': 'sem resposta', '000': 'sem resposta'}.get(c := sh(n, f"curl -s -m 6 -o /dev/null -w '%{{http_code}}' {url}"), c)
    sh('PC-NAV-HQ', f"curl -s -m 10 -X POST -d '' {PORTAL}/logoff/0")
    chk('PC-NAV-HQ -> PC-USUARIO (mesma VLAN, DAI)', ping('PC-NAV-HQ', '10.10.10.11'), 'passa')
    chk('PC-NAV-HQ sem sessão -> aplicação', http('PC-NAV-HQ', f'http://{APLICACAO}/'), '302')
    r = sh('PC-NAV-HQ', f"curl -s -m 15 -X POST -d 'user=usuario1&password=Senha.Tcc1' {PORTAL}/logon/0")
    chk('PC-NAV-HQ login no portal', 'AUTHORIZED' if 'AUTHORIZED' in r.replace('NOT_AUTHORIZED', '') else r[:80], 'AUTHORIZED')
    chk('PC-NAV-HQ com sessão -> aplicação HTTP', http('PC-NAV-HQ', f'http://{APLICACAO}/'), '200')
    chk('PC-NAV-HQ com sessão -> aplicação HTTPS', http('PC-NAV-HQ', f'-k https://{APLICACAO}/'), '200')
    chk('PC-NAV-HQ com sessão -> SSH no servidor (sem regra)',
        'passa' if 'open' in sh('PC-NAV-HQ', f'timeout 5 bash -c "echo > /dev/tcp/{APLICACAO}/22" && echo open || echo fechado') else 'bloqueado', 'bloqueado')
    sh('PC-NAV-HQ', f"curl -s -m 10 -X POST -d '' {PORTAL}/logoff/0")             # sem sessão: o login fica para o teste visual
    chk('PC-NAV-F1 -> PC-FIL1 (mesma VLAN, DAI)', ping('PC-NAV-F1', '10.20.10.11'), 'passa')
    chk('PC-NAV-F1 -> aplicação da matriz', http('PC-NAV-F1', f'http://{APLICACAO}/'), 'sem resposta')
    chk('PC-NAV-F2 -> PC-FIL2 (mesma VLAN, DAI)', ping('PC-NAV-F2', '10.30.10.11'), 'passa')
    chk('PC-NAV-F2 -> aplicação da matriz', http('PC-NAV-F2', f'http://{APLICACAO}/'), 'sem resposta')
    texto = '\n'.join(res)
    (PASTA / 'teste_funcional.txt').write_text(texto + '\n', encoding='utf-8')
    log('teste:\n' + texto)


def passo_backup():
    p = proj(); N = nos(p)
    for sw in ('SW-ACC1', 'SW-FIL1', 'SW-FIL2'):
        con = g.Console(p, N[sw]); assert g.cisco_pronto(con, 60)
        (PASTA / f'{sw}.cfg').write_text(g.cisco_show(con, 'show running-config', 12), encoding='utf-8')
    g.OpnAPIGer(CHAVES['etapa0-FW-HQ']).backup(PASTA / 'FW-HQ.xml')
    log('configurações salvas em', PASTA)


PASSOS = ['duplicar', 'nos', 'ligar', 'l2', 'dhcp', 'firewall', 'rotulos', 'teste', 'backup']
if __name__ == '__main__':
    for nome in (sys.argv[1:] or PASSOS):
        log('==', nome); globals()['passo_' + nome]()
