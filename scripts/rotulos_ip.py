"""Coloca no desenho do projeto do GNS3 uma anotação com as interfaces e os IPs de cada equipamento.

Uso: python rotulos_ip.py TCC-etapa-0
As anotações são só visuais (drawings do GNS3). Ao rodar de novo, as anteriores criadas por este script são
substituídas (ids guardados em lab/<pasta da etapa>/rotulos_ip.json). Arraste-as na interface se quiser.
"""
import json, pathlib, sys
from xml.sax.saxutils import escape
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import gns3lab as g

PROJ = sys.argv[1] if len(sys.argv) > 1 else 'TCC-etapa-0'
RAIZ = pathlib.Path(__file__).resolve().parents[1]
PASTA = RAIZ / PROJ.replace('TCC-', '').lower()
PASTA.mkdir(exist_ok=True)

ROTULOS = {
    'TCC-etapa-0': {
        'PROVEDOR':      ['eth0 172.16.0.1/30 (R-HQ)', 'eth1 172.16.0.5/30 (R-FIL1)', 'eth2 172.16.0.9/30 (R-FIL2)', 'eth3 DHCP (internet)'],
        'R-HQ':          ['e0/0 172.16.0.2/30', 'e0/1 10.255.1.1/30'],
        'R-FIL1':        ['e0/0 172.16.0.6/30', 'e0/1 10.255.2.1/30'],
        'R-FIL2':        ['e0/0 172.16.0.10/30', 'e0/1 10.255.3.1/30'],
        'FW-HQ':         ['WAN vtnet1 10.255.1.2/30', 'LAN vtnet0 10.10.10.1/24', 'GER vtnet2 192.168.16.31/24'],
        'FW-F1':         ['WAN vtnet1 10.255.2.2/30', 'LAN vtnet0 10.20.10.1/24', 'GER vtnet2 192.168.16.32/24'],
        'FW-F2':         ['WAN vtnet1 10.255.3.2/30', 'LAN vtnet0 10.30.10.1/24', 'GER vtnet2 192.168.16.33/24'],
        'SW-CORE':       ['L2, VLAN 1 (rede plana)', 'ger. 10.10.10.2/24 (Telnet)'],
        'SW-ACC1':       ['L2, VLAN 1', 'ger. 10.10.10.3/24 (Telnet)'],
        'SW-ACC2':       ['L2, VLAN 1', 'ger. 10.10.10.4/24 (Telnet)'],
        'SW-FIL1':       ['L2, VLAN 1', 'ger. 10.20.10.2/24 (Telnet)'],
        'SW-FIL2':       ['L2, VLAN 1', 'ger. 10.30.10.2/24 (Telnet)'],
        'PC-USUARIO':    ['10.10.10.11/24', 'gw 10.10.10.1'],
        'HOST-INVADIDO': ['10.10.10.12/24', 'gw 10.10.10.1'],
        'APLICACAO':     ['10.10.10.21/24', 'gw 10.10.10.1', 'HTTP/HTTPS, SSH'],
        'ARQUIVOS':      ['10.10.10.22/24', 'gw 10.10.10.1', 'SMB, SSH'],
        'PC-FIL1':       ['10.20.10.11/24', 'gw 10.20.10.1'],
        'PC-FIL2':       ['10.30.10.11/24', 'gw 10.30.10.1'],
        'MGMT-SW':       ['192.168.16.0/24 (rede do Windows)'],
    },
}
# lado da anotação em relação ao ícone (padrão: direita)
LADO = {'HOST-INVADIDO': 'abaixo', 'PC-USUARIO': 'abaixo', 'APLICACAO': 'abaixo', 'ARQUIVOS': 'abaixo',
        'SW-ACC1': 'esquerda', 'R-HQ': 'esquerda', 'FW-HQ': 'esquerda', 'SW-CORE': 'esquerda', 'PROVEDOR': 'direita'}

p = g.Projeto(PROJ)
arq = PASTA / 'rotulos_ip.json'
if arq.exists():
    for did in json.loads(arq.read_text()):
        try:
            g.api('DELETE', f'/projects/{p.id}/drawings/{did}')
        except Exception:
            pass
nos = {n['name']: n for n in g.api('GET', f'/projects/{p.id}/nodes')}
criados = []
for nome, linhas in ROTULOS[PROJ].items():
    n = nos.get(nome)
    if not n:
        continue
    fs = 10
    w = max(len(l) for l in linhas) * 6.2 + 10
    h = len(linhas) * (fs + 4) + 6
    lado = LADO.get(nome, 'direita')
    nw, nh = n.get('width') or 60, n.get('height') or 45
    if lado == 'esquerda':
        x, y = n['x'] - w - 6, n['y']
    elif lado == 'abaixo':
        x, y = n['x'] - (w - nw) / 2, n['y'] + nh + 18
    else:
        x, y = n['x'] + nw + 6, n['y']
    tspans = ''.join(f'<tspan x="0" dy="{fs + 4 if i else fs}">{escape(l)}</tspan>' for i, l in enumerate(linhas))
    svg = (f'<svg width="{w:.0f}" height="{h:.0f}"><text font-family="Consolas" font-size="{fs}" fill="#1f3a93" '
           f'fill-opacity="1.0">{chr(10).join(escape(l) for l in linhas)}</text></svg>')
    d = g.api('POST', f'/projects/{p.id}/drawings', {'x': int(x), 'y': int(y), 'z': 2, 'svg': svg})
    criados.append(d['drawing_id'])
arq.write_text(json.dumps(criados))
print(f'{len(criados)} anotações de IP colocadas no projeto {PROJ}')
