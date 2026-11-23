"""Etapa A — modelo de segurança perimetral, a partir do TCC-etapa-A (duplicado do TCC-etapa-0).

Uso: python montar_etapaA.py            (o projeto TCC-etapa-A já deve existir, duplicado do TCC-etapa-0, e estar ligado)

Matriz em VLANs, roteadas pelo SW-CORE (interior livre); firewalls filtrando só a WAN (borda):
  VLAN 10 Usuários   10.10.10.0/24  gateway SW-CORE 10.10.10.1 (PC-USUARIO .11, HOST-INVADIDO .12 por DHCP com reserva)
  VLAN 20 Servidores 10.10.20.0/24  gateway SW-CORE 10.10.20.1 (APLICACAO .21, ARQUIVOS .22, IP fixo)
  VLAN 99 Gerência   10.10.99.0/24  SW-CORE .1, SW-ACC1 .3, SW-ACC2 .4 (Telnet)
  VLAN 100 Trânsito  10.10.100.0/30 FW-HQ .1, SW-CORE .2 — nativa (sem etiqueta) no trunk SW-CORE e0/0 ↔ FW-HQ vtnet0;
                     na etapa B1 a VLAN 20 entra etiquetada no mesmo trunk.
  DHCP: dnsmasq do FW-HQ, faixa relayed 10.10.10.100–199 e reservas por MAC; relay (ip helper-address) na SVI da VLAN 10.
  FW-HQ: rota 10.10.0.0/16 via SW-CORE (10.10.100.2); LAN aceita 10.10.0.0/16.
  WAN dos três firewalls: só 10.0.0.0/8 (unidades da empresa) → rede da própria unidade; o resto é bloqueado
  (inclusive o próprio firewall pela WAN). Filiais: sem mudança interna (uma rede só).
Configurações exportadas para lab/etapa-A/. Não digite nos consoles enquanto o script roda.
"""
import json, pathlib, re, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import gns3lab as g

def log(*a): print(time.strftime('%H:%M:%S'), *a, flush=True)
RAIZ = pathlib.Path(__file__).resolve().parents[1]
ET = RAIZ / 'etapa-A'; ET.mkdir(exist_ok=True)
CHAVES = json.loads((RAIZ / 'dados' / 'opnsense_api_keys.json').read_text())
p = g.Projeto('TCC-etapa-A')
N = {n['name']: n for n in g.api('GET', f'/projects/{p.id}/nodes')}
UNIDADES = {'FW-HQ': '10.10.0.0/16', 'FW-F1': '10.20.0.0/16', 'FW-F2': '10.30.0.0/16'}
API = {fw: g.OpnAPIGer(CHAVES[f'etapa0-{fw}']) for fw in UNIDADES}

# ------------------------------------------------------------------ 1) FW-HQ: LAN vira trânsito, rota de volta, DHCP
hq = API['FW-HQ']
try:
    lan_atual = json.dumps(hq('GET', 'interfaces/overview/interfaces_info'))
except Exception:
    lan_atual = ''
if '10.10.100.1' not in lan_atual:
    con = g.Console(p, N['FW-HQ'])
    assert g.opn_menu(con, 300) and g.opn_ip(con, 'LAN', '10.10.100.1', 30), 'FW-HQ: LAN'
    log('FW-HQ: LAN 10.10.100.1/30 (trânsito)')
gws = {r['name']: r for r in hq('GET', 'routing/settings/search_gateway')['rows']}
if 'SWCORE_GW' not in gws:
    r = hq('POST', 'routing/settings/add_gateway', {'gateway_item': {'disabled': '0', 'name': 'SWCORE_GW', 'descr': 'SW-CORE (VLANs da matriz)',
        'interface': 'lan', 'ipprotocol': 'inet', 'gateway': '10.10.100.2', 'defaultgw': '0', 'monitor_disable': '1'}})
    assert r.get('result') == 'saved', r
# o gateway novo só aparece como opção de rota depois de aplicado (alguns segundos)
for _ in range(12):
    hq('POST', 'routing/settings/reconfigure', {}); time.sleep(5)
    if 'SWCORE_GW' in hq('GET', 'routes/routes/getroute')['route']['gateway']:
        break
if not any(r.get('network') == '10.10.0.0/16' for r in hq('GET', 'routes/routes/searchroute')['rows']):
    r = hq('POST', 'routes/routes/addroute', {'route': {'network': '10.10.0.0/16', 'gateway': 'SWCORE_GW', 'descr': 'VLANs da matriz', 'enabled': '1'}})
    assert r.get('result') == 'saved', r
    hq('POST', 'routes/routes/reconfigure', {})
log('FW-HQ: gateway SWCORE_GW 10.10.100.2 e rota 10.10.0.0/16')

# ------------------------------------------------------------------ 2) regras dos três firewalls
for fw, rede in UNIDADES.items():
    a = API[fw]
    n = a.apagar_regras('Etapa 0') + a.apagar_regras('Etapa A')
    a.regra('wan', '10.0.0.0/8', rede, f'Etapa A: unidades da empresa -> rede da unidade ({rede})')
    if fw == 'FW-HQ':
        a.regra('lan', '10.10.0.0/16', 'any', 'Etapa A: VLANs da matriz (via SW-CORE) -> qualquer')
    a('POST', 'firewall/filter/apply', {})
    log(f'{fw}: {n} regra(s) antiga(s) removida(s); WAN só 10.0.0.0/8 -> {rede}')

# ------------------------------------------------------------------ 3) switches da matriz
VTP = 'vtp mode transparent'
SEM_GER_ANTIGA = 'interface Vlan1\n no ip address\n shutdown\nexit\nno ip default-gateway\n'
CFG = {
'SW-CORE': f"""{VTP}
vlan 10
 name USUARIOS
vlan 20
 name SERVIDORES
vlan 99
 name GERENCIA
vlan 100
 name TRANSITO
exit
{SEM_GER_ANTIGA}no ip route 0.0.0.0 0.0.0.0 10.10.10.1
ip routing
interface Vlan10
 ip address 10.10.10.1 255.255.255.0
 ip helper-address 10.10.100.1
 no shutdown
interface Vlan20
 ip address 10.10.20.1 255.255.255.0
 no shutdown
interface Vlan99
 ip address 10.10.99.1 255.255.255.0
 no shutdown
interface Vlan100
 ip address 10.10.100.2 255.255.255.252
 no shutdown
interface Ethernet0/0
 description FW-HQ (trunk; VLAN 100 nativa)
 switchport trunk encapsulation dot1q
 switchport trunk native vlan 100
 switchport trunk allowed vlan 100
 switchport mode trunk
interface Ethernet0/1
 description SW-ACC1 (trunk)
 switchport trunk encapsulation dot1q
 switchport trunk allowed vlan 10,99
 switchport mode trunk
interface Ethernet0/2
 description SW-ACC2 (trunk)
 switchport trunk encapsulation dot1q
 switchport trunk allowed vlan 20,99
 switchport mode trunk
exit
ip route 0.0.0.0 0.0.0.0 10.10.100.1""",
'SW-ACC1': f"""{VTP}
vlan 10
 name USUARIOS
vlan 99
 name GERENCIA
exit
{SEM_GER_ANTIGA}no ip route 0.0.0.0 0.0.0.0 10.10.10.1
interface Vlan99
 ip address 10.10.99.3 255.255.255.0
 no shutdown
interface Ethernet0/0
 description SW-CORE (trunk)
 switchport trunk encapsulation dot1q
 switchport trunk allowed vlan 10,99
 switchport mode trunk
interface range Ethernet0/1 - 2
 switchport mode access
 switchport access vlan 10
exit
ip route 0.0.0.0 0.0.0.0 10.10.99.1""",
'SW-ACC2': f"""{VTP}
vlan 20
 name SERVIDORES
vlan 99
 name GERENCIA
exit
{SEM_GER_ANTIGA}no ip route 0.0.0.0 0.0.0.0 10.10.10.1
interface Vlan99
 ip address 10.10.99.4 255.255.255.0
 no shutdown
interface Ethernet0/0
 description SW-CORE (trunk)
 switchport trunk encapsulation dot1q
 switchport trunk allowed vlan 20,99
 switchport mode trunk
interface range Ethernet0/1 - 2
 switchport mode access
 switchport access vlan 20
exit
ip route 0.0.0.0 0.0.0.0 10.10.99.1""",
}
for sw, cfg in CFG.items():
    con = g.Console(p, N[sw]); assert g.cisco_pronto(con, 60), sw
    g.cisco_config(con, cfg, espera=0.6)
    assert g.cisco_salvar(con), f'{sw}: write memory'
    log(f'{sw}: VLANs e gerência na VLAN 99 configuradas e salvas')

# ------------------------------------------------------------------ 4) servidores na VLAN 20
for h, ip in (('APLICACAO', '10.10.20.21'), ('ARQUIVOS', '10.10.20.22')):
    iface = f'auto eth0\niface eth0 inet static\n\taddress {ip}\n\tnetmask 255.255.255.0\n\tgateway 10.10.20.1\n'
    g.api('POST', f"/projects/{p.id}/nodes/{N[h]['node_id']}/files/etc/network/interfaces", bruto=iface)
    p.parar(N[h]); time.sleep(2); p.iniciar(N[h])
    log(f'{h}: {ip}/24, gateway 10.10.20.1')

# ------------------------------------------------------------------ 5) DHCP com relay para a VLAN 10 (dnsmasq do FW-HQ)
RESERVAS = {'PC-USUARIO': '10.10.10.11', 'HOST-INVADIDO': '10.10.10.12'}
if not hq('GET', 'dnsmasq/settings/search_range')['rows']:
    r = hq('POST', 'dnsmasq/settings/add_range', {'range': {'interface': '', 'start_addr': '10.10.10.100', 'end_addr': '10.10.10.199',
                                                            'subnet_mask': '255.255.255.0', 'description': 'VLAN 10 Usuarios (relay do SW-CORE)'}})
    assert r.get('result') == 'saved', r
hosts_atuais = {h.get('host') for h in hq('GET', 'dnsmasq/settings/search_host')['rows']}
for h, ip in RESERVAS.items():
    mac = g.vm(f"docker exec {g.conteiner(p, N[h])} cat /sys/class/net/eth0/address").strip()
    nome = h.lower()
    if nome not in hosts_atuais:
        r = hq('POST', 'dnsmasq/settings/add_host', {'host': {'host': nome, 'ip': ip, 'hwaddr': mac, 'descr': f'{h} (reserva)'}})
        assert r.get('result') == 'saved', r
    log(f'reserva DHCP: {h} {mac} -> {ip}')
hq('POST', 'dnsmasq/service/reconfigure', {})
for h in RESERVAS:
    g.api('POST', f"/projects/{p.id}/nodes/{N[h]['node_id']}/files/etc/network/interfaces", bruto='auto eth0\niface eth0 inet dhcp\n')
    p.parar(N[h]); time.sleep(2); p.iniciar(N[h])
time.sleep(20)
for h, ip in RESERVAS.items():
    c = g.conteiner(p, N[h])
    obtido = g.vm(f"docker exec {c} sh -c \"ip -4 -o addr show eth0 | awk '{{print \\$4}}'; ip route | awk '/default/{{print \\$3}}'\"").split()
    log(f'{h}: DHCP -> {obtido}', 'OK' if obtido[:1] == [f'{ip}/24'] else 'ATENÇÃO')

# ------------------------------------------------------------------ 6) backups e configurações
for fw in UNIDADES:
    API[fw].backup(ET / f'{fw}.xml')
for nome in ('R-HQ', 'R-FIL1', 'R-FIL2', 'SW-CORE', 'SW-ACC1', 'SW-ACC2', 'SW-FIL1', 'SW-FIL2'):
    con = g.Console(p, N[nome]); g.cisco_pronto(con, 60)
    run = g.cisco_show(con, 'show running-config', 6)
    (ET / f'{nome}.cfg').write_text(run[run.find('Building configuration'):] if 'Building configuration' in run else run, encoding='utf-8')
log('backups em lab/etapa-A/')

# ------------------------------------------------------------------ 7) teste funcional
IPS = {'PC-USUARIO': '10.10.10.11', 'HOST-INVADIDO': '10.10.10.12', 'APLICACAO': '10.10.20.21', 'ARQUIVOS': '10.10.20.22',
       'PC-FIL1': '10.20.10.11', 'PC-FIL2': '10.30.10.11'}
linhas = []
for origem in ('PC-USUARIO', 'HOST-INVADIDO', 'APLICACAO', 'PC-FIL1', 'PC-FIL2'):
    co = g.conteiner(p, N[origem])
    for destino, ip in IPS.items():
        if destino == origem: continue
        out = g.vm(f'docker exec {co} ping -c 3 -i 0.3 -W 3 {ip} | tail -2')
        m = re.search(r'([\d.]+)% packet loss', out); rtt = re.search(r'= [\d.]+/([\d.]+)/', out)
        linha = f"{origem:14s} -> {destino:14s} perda {m.group(1) if m else '?':>3}%  RTT médio {rtt.group(1) if rtt else '-'} ms"
        linhas.append(linha); log(linha)
(ET / 'teste_funcional.txt').write_text('\n'.join(linhas), encoding='utf-8')
log('etapa A montada')
