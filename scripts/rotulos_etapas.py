"""Atualiza as anotações do desenho de um projeto do GNS3 para a configuração da etapa (para o print de cada etapa).

Uso: python rotulos_etapas.py TCC-etapa-A        (TCC-etapa-0, TCC-etapa-A, TCC-etapa-B1, TCC-etapa-B2)
- Reescreve no lugar as anotações de IP já existentes (as que o rotulos_ip.py criou na etapa 0 e que a duplicação
  copiou), mantendo as posições arrumadas na interface; cria as que faltarem.
- Acrescenta (ou atualiza) um quadro com o nome da etapa e os controles ativos, no canto superior esquerdo.
Rode com a bateria de ensaio parada: mexer no projeto durante a medição altera a CPU medida.
"""
import html, json, math, pathlib, re, sys
from xml.sax.saxutils import escape
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import gns3lab as g

PROJ = sys.argv[1] if len(sys.argv) > 1 else 'TCC-etapa-A'
RAIZ = pathlib.Path(__file__).resolve().parents[1]
PASTA = RAIZ / PROJ.replace('TCC-', '').lower(); PASTA.mkdir(exist_ok=True)

BASE = {  # comum a todas as etapas
    'PROVEDOR': ['eth0 172.16.0.1/30 (R-HQ)', 'eth1 172.16.0.5/30 (R-FIL1)', 'eth2 172.16.0.9/30 (R-FIL2)', 'eth3 DHCP (internet)'],
    'R-HQ': ['e0/0 172.16.0.2/30', 'e0/1 10.255.1.1/30'],
    'R-FIL1': ['e0/0 172.16.0.6/30', 'e0/1 10.255.2.1/30'],
    'R-FIL2': ['e0/0 172.16.0.10/30', 'e0/1 10.255.3.1/30'],
    'PC-FIL1': ['10.20.10.11/24', 'gw 10.20.10.1'],
    'PC-FIL2': ['10.30.10.11/24', 'gw 10.30.10.1'],
    'MGMT-SW': ['192.168.16.0/24 (rede do Windows)'],
}
ETAPAS = {
    'TCC-etapa-0': ('Etapa 0 — rede plana', ['uma sub-rede por unidade', 'firewalls liberam todo o tráfego', 'gerência dos Cisco por Telnet'], {
        'FW-HQ': ['WAN vtnet1 10.255.1.2/30', 'LAN vtnet0 10.10.10.1/24', 'GER vtnet2 192.168.16.31/24', 'libera tudo'],
        'FW-F1': ['WAN vtnet1 10.255.2.2/30', 'LAN vtnet0 10.20.10.1/24', 'GER vtnet2 192.168.16.32/24', 'libera tudo'],
        'FW-F2': ['WAN vtnet1 10.255.3.2/30', 'LAN vtnet0 10.30.10.1/24', 'GER vtnet2 192.168.16.33/24', 'libera tudo'],
        'SW-CORE': ['L2, VLAN 1 (rede plana)', 'ger. 10.10.10.2/24 (Telnet)'],
        'SW-ACC1': ['L2, VLAN 1', 'ger. 10.10.10.3/24 (Telnet)'],
        'SW-ACC2': ['L2, VLAN 1', 'ger. 10.10.10.4/24 (Telnet)'],
        'SW-FIL1': ['L2, VLAN 1', 'ger. 10.20.10.2/24 (Telnet)'],
        'SW-FIL2': ['L2, VLAN 1', 'ger. 10.30.10.2/24 (Telnet)'],
        'PC-USUARIO': ['10.10.10.11/24', 'gw 10.10.10.1'],
        'HOST-INVADIDO': ['10.10.10.12/24', 'gw 10.10.10.1'],
        'APLICACAO': ['10.10.10.21/24', 'gw 10.10.10.1', 'HTTP/HTTPS, SSH'],
        'ARQUIVOS': ['10.10.10.22/24', 'gw 10.10.10.1', 'SMB, SSH'],
    }),
    'TCC-etapa-A': ('Etapa A — modelo perimetral', ['VLANs 10, 20, 99 e 100 na matriz', 'SW-CORE roteia as VLANs sem restrição',
                                                    'firewalls filtram só a WAN', 'DHCP da VLAN 10 por relay', 'gerência dos Cisco por Telnet'], {
        'FW-HQ': ['WAN vtnet1 10.255.1.2/30', 'LAN vtnet0 10.10.100.1/30 (trânsito)', 'GER vtnet2 192.168.16.31/24', 'filtra só a WAN; DHCP (relay)'],
        'FW-F1': ['WAN vtnet1 10.255.2.2/30', 'LAN vtnet0 10.20.10.1/24', 'GER vtnet2 192.168.16.32/24', 'filtra só a WAN'],
        'FW-F2': ['WAN vtnet1 10.255.3.2/30', 'LAN vtnet0 10.30.10.1/24', 'GER vtnet2 192.168.16.33/24', 'filtra só a WAN'],
        'SW-CORE': ['L3: roteia as VLANs', 'Vlan10 10.10.10.1/24', 'Vlan20 10.10.20.1/24', 'Vlan99 10.10.99.1/24', 'Vlan100 10.10.100.2/30'],
        'SW-ACC1': ['VLAN 10 (usuários)', 'ger. 10.10.99.3/24 (Telnet)'],
        'SW-ACC2': ['VLAN 20 (servidores)', 'ger. 10.10.99.4/24 (Telnet)'],
        'SW-FIL1': ['L2, VLAN 1', 'ger. 10.20.10.2/24 (Telnet)'],
        'SW-FIL2': ['L2, VLAN 1', 'ger. 10.30.10.2/24 (Telnet)'],
        'PC-USUARIO': ['10.10.10.11/24 (DHCP)', 'gw 10.10.10.1'],
        'HOST-INVADIDO': ['10.10.10.12/24 (DHCP)', 'gw 10.10.10.1'],
        'APLICACAO': ['10.10.20.21/24', 'gw 10.10.20.1', 'HTTP/HTTPS, SSH'],
        'ARQUIVOS': ['10.10.20.22/24', 'gw 10.10.20.1', 'SMB, SSH'],
    }),
    'TCC-etapa-B1': ('Etapa B1 — Zero Trust', ['servidores em enclave (gateway no FW-HQ)', 'bloqueio padrão nos três firewalls',
                                               'portal cativo + FreeRADIUS', 'ACL no SW-CORE; DAI e port security',
                                               'gerência por SSH + AAA'], {
        'FW-HQ': ['WAN vtnet1 10.255.1.2/30', 'LAN vtnet0 10.10.100.1/30 (trânsito)', 'SERVIDORES vlan01 (tag 20) 10.10.20.1/24',
                  'GER vtnet2 192.168.16.31/24', 'bloqueio padrão; portal; RADIUS'],
        'FW-F1': ['WAN vtnet1 10.255.2.2/30', 'LAN vtnet0 10.20.10.1/24', 'GER vtnet2 192.168.16.32/24', 'bloqueio padrão'],
        'FW-F2': ['WAN vtnet1 10.255.3.2/30', 'LAN vtnet0 10.30.10.1/24', 'GER vtnet2 192.168.16.33/24', 'bloqueio padrão'],
        'SW-CORE': ['L3: Vlan10 10.10.10.1/24 (ACL)', 'Vlan99 10.10.99.1/24', 'Vlan100 10.10.100.2/30', 'VLAN 20 só L2 (enclave)', 'SSH + AAA (RADIUS)'],
        'SW-ACC1': ['VLAN 10; DAI, port security', 'ger. 10.10.99.3/24 (SSH)'],
        'SW-ACC2': ['VLAN 20; DAI, port security', 'ger. 10.10.99.4/24 (SSH)'],
        'SW-FIL1': ['VLAN 1; DAI, port security', 'ger. 10.20.10.2/24 (SSH)'],
        'SW-FIL2': ['VLAN 1; DAI, port security', 'ger. 10.30.10.2/24 (SSH)'],
        'PC-USUARIO': ['10.10.10.11/24 (DHCP)', 'gw 10.10.10.1', 'login no portal cativo'],
        'HOST-INVADIDO': ['10.10.10.12/24 (DHCP)', 'gw 10.10.10.1', 'sem login'],
        'APLICACAO': ['10.10.20.21/24', 'gw 10.10.20.1 (FW-HQ)', 'HTTP/HTTPS, SSH'],
        'ARQUIVOS': ['10.10.20.22/24', 'gw 10.10.20.1 (FW-HQ)', 'SMB, SSH'],
    }),
}
ETAPAS['TCC-etapa-B1'][2].update({'R-HQ': BASE['R-HQ'] + ['SSH + AAA'], 'R-FIL1': BASE['R-FIL1'] + ['SSH + AAA'],
                                  'R-FIL2': BASE['R-FIL2'] + ['SSH + AAA']})

COR = '#1f3a93'


def svg_texto(linhas, fs=10, negrito_primeira=False):
    w = max(len(l) for l in linhas) * 6.2 + 10
    h = len(linhas) * (fs + 4) + 6
    corpo = chr(10).join(escape(l) for l in linhas)
    return (f'<svg width="{w:.0f}" height="{h:.0f}"><text font-family="Consolas" font-size="{fs}" fill="{COR}" '
            f'fill-opacity="1.0">{corpo}</text></svg>')


def svg_quadro(titulo, itens):
    linhas = [titulo] + ['• ' + i for i in itens]
    w = max(len(l) for l in linhas) * 7.4 + 24
    h = 22 + len(itens) * 16 + 12
    t = (f'<svg width="{w:.0f}" height="{h:.0f}"><rect x="1" y="1" width="{w - 2:.0f}" height="{h - 2:.0f}" rx="6" '
         f'fill="#ffffff" fill-opacity="0.9" stroke="{COR}" stroke-width="1.5"/>'
         f'<text x="10" y="18" font-family="Arial" font-size="13" font-weight="bold" fill="{COR}">{escape(titulo)}</text>')
    for k, i in enumerate(itens):
        t += f'<text x="12" y="{36 + k * 16}" font-family="Arial" font-size="11" fill="#222">{escape("• " + i)}</text>'
    return t + '</svg>'


titulo, itens, especificos = ETAPAS[PROJ]
rotulos = dict(BASE); rotulos.update(especificos)
p = g.Projeto(PROJ)
nos = {n['name']: n for n in g.api('GET', f'/projects/{p.id}/nodes')}
desenhos = g.api('GET', f'/projects/{p.id}/drawings')
anot = [d for d in desenhos if 'font-family="Consolas"' in d['svg'] and COR in d['svg']]
# cada equipamento fica com a anotação cujo texto é dele (linhas em comum com os rótulos desse equipamento em qualquer
# etapa); a distância só desempata. Só pela distância, a anotação do SW-CORE (à esquerda dele) foi parar no SW-ACC1
# na etapa B1, e a do SW-ACC1 ficou com o texto da etapa 0.
def linhas_svg(svg):
    m = re.search(r'<text[^>]*>(.*?)</text>', svg, re.S)
    return {html.unescape(l).strip() for l in m.group(1).split('\n')} if m else set()


assinatura = {n: set(BASE.get(n, [])) | {l for _, _, esp in ETAPAS.values() for l in esp.get(n, [])} for n in rotulos}
pares = sorted(((-len(linhas_svg(d['svg']) & assinatura[n]), math.hypot(d['x'] - nos[n]['x'], d['y'] - nos[n]['y']), n, d['drawing_id'])
                for n in rotulos if n in nos for d in anot), key=lambda x: (x[0], x[1]))
usado_no, usado_d, alvo = set(), set(), {}
for comum, dist, n, did in pares:
    if n in usado_no or did in usado_d or (comum == 0 and dist > 320):
        continue
    alvo[n] = did; usado_no.add(n); usado_d.add(did)
sobras = [d['drawing_id'][:8] for d in anot if d['drawing_id'] not in usado_d]
if sobras:
    print('anotações sem equipamento (conferir na interface):', sobras)
criados = 0
for n, linhas in rotulos.items():
    if n not in nos:
        continue
    if n in alvo:
        g.api('PUT', f'/projects/{p.id}/drawings/{alvo[n]}', {'svg': svg_texto(linhas)})
    else:
        nn = nos[n]
        g.api('POST', f'/projects/{p.id}/drawings', {'x': int(nn['x'] + (nn.get('width') or 60) + 6), 'y': int(nn['y']), 'z': 2,
                                                     'svg': svg_texto(linhas)})
        criados += 1
# quadro da etapa
reg = PASTA / 'quadro_etapa.json'
qid = json.loads(reg.read_text()).get('id') if reg.exists() else None
existentes = {d['drawing_id'] for d in desenhos}
xmin = min(n['x'] for n in nos.values()) - 40; ymin = min(n['y'] for n in nos.values()) - 40
if qid in existentes:
    g.api('PUT', f'/projects/{p.id}/drawings/{qid}', {'svg': svg_quadro(titulo, itens)})
else:
    d = g.api('POST', f'/projects/{p.id}/drawings', {'x': int(xmin), 'y': int(ymin - 140), 'z': 3, 'svg': svg_quadro(titulo, itens)})
    reg.write_text(json.dumps({'id': d['drawing_id']}))
print(f'{PROJ}: {len(alvo)} anotações reescritas no lugar, {criados} criadas; quadro "{titulo}"')
