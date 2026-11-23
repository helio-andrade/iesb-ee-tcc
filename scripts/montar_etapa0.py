"""Fase 2 — monta o projeto TCC-etapa-0 (topologia completa, rede plana) a partir dos templates "TCC -".

Matriz: R-HQ, FW-HQ, SW-CORE, SW-ACC1, SW-ACC2, PC-USUARIO, HOST-INVADIDO, APLICACAO, ARQUIVOS
Filial 1: R-FIL1, FW-F1, SW-FIL1, PC-FIL1   |   Filial 2: R-FIL2, FW-F2, SW-FIL2, PC-FIL2
PROVEDOR (contêiner): roteia, aplica tc/netem (RTT 20 ms/20 Mbit/s e 60 ms/10 Mbit/s) e dá internet (nó NAT).
Gerência: nó Cloud no eth0 da GNS3 VM + MGMT-SW (FW-HQ .31, FW-F1 .32, FW-F2 .33 em 192.168.16.0/24).
Etapa 0 = rede plana: uma sub-rede por unidade, firewalls liberando tudo, sem NAT entre unidades.
Configurações salvas em lab/etapa-0/.
"""
import json, pathlib, re, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import gns3lab as g

def log(*a): print(time.strftime('%H:%M:%S'), *a, flush=True)
RAIZ = pathlib.Path(__file__).resolve().parents[1]
ET = RAIZ / 'etapa-0'; ET.mkdir(exist_ok=True)
CHAVES = RAIZ / 'dados' / 'opnsense_api_keys.json'
SRV = ':/symbols/classic/server.svg'

# ------------------------------------------------------------------ plano de endereços
SITES = {
    'HQ':  dict(r='R-HQ',   fw='FW-HQ', prov=('172.16.0.1', '172.16.0.2'),  wan=('10.255.1.1', '10.255.1.2'),
                lan='10.10.10.1', rede='10.10.0.0/16', mgmt='192.168.16.31', apih='PC-USUARIO'),
    'F1':  dict(r='R-FIL1', fw='FW-F1', prov=('172.16.0.5', '172.16.0.6'),  wan=('10.255.2.1', '10.255.2.2'),
                lan='10.20.10.1', rede='10.20.0.0/16', mgmt='192.168.16.32', apih='PC-FIL1'),
    'F2':  dict(r='R-FIL2', fw='FW-F2', prov=('172.16.0.9', '172.16.0.10'), wan=('10.255.3.1', '10.255.3.2'),
                lan='10.30.10.1', rede='10.30.0.0/16', mgmt='192.168.16.33', apih='PC-FIL2'),
}
HOSTS = {  # nome: (ip, gateway, switch, porta, x, y, símbolo)
    'PC-USUARIO':    ('10.10.10.11', '10.10.10.1', 'SW-ACC1', (0, 1), -700, 280, None),
    'HOST-INVADIDO': ('10.10.10.12', '10.10.10.1', 'SW-ACC1', (0, 2), -560, 280, None),
    'APLICACAO':     ('10.10.10.21', '10.10.10.1', 'SW-ACC2', (0, 1), -380, 280, SRV),
    'ARQUIVOS':      ('10.10.10.22', '10.10.10.1', 'SW-ACC2', (0, 2), -240, 280, SRV),
    'PC-FIL1':       ('10.20.10.11', '10.20.10.1', 'SW-FIL1', (0, 1),  100, 140, None),
    'PC-FIL2':       ('10.30.10.11', '10.30.10.1', 'SW-FIL2', (0, 1),  400, 140, None),
}

PROVEDOR_SH = r'''#!/bin/sh
# PROVEDOR (etapa 0): roteamento entre as unidades, internet pelo nó NAT e perfis de enlace (tc/netem).
sysctl -w net.ipv4.ip_forward=1 >/dev/null
ip route replace 10.10.0.0/16  via 172.16.0.2
ip route replace 10.255.1.0/30 via 172.16.0.2
ip route replace 10.20.0.0/16  via 172.16.0.6
ip route replace 10.255.2.0/30 via 172.16.0.6
ip route replace 10.30.0.0/16  via 172.16.0.10
ip route replace 10.255.3.0/30 via 172.16.0.10
iptables -t nat -C POSTROUTING -o eth3 -j MASQUERADE 2>/dev/null || iptables -t nat -A POSTROUTING -o eth3 -j MASQUERADE
# perfil(dev, taxa, atraso_por_sentido): RTT = 2 x atraso (simétrico: netem na saída + IFB na entrada)
perfil() {
  dev=$1; taxa=$2; atraso=$3; ifb=ifb-$dev
  tc qdisc del dev $dev root 2>/dev/null; tc qdisc del dev $dev ingress 2>/dev/null
  ip link del $ifb 2>/dev/null
  tc qdisc add dev $dev root handle 1: htb default 10
  tc class add dev $dev parent 1: classid 1:10 htb rate $taxa ceil $taxa
  tc qdisc add dev $dev parent 1:10 handle 10: netem delay $atraso limit 10000
  ip link add $ifb type ifb && ip link set $ifb up
  tc qdisc add dev $dev handle ffff: ingress
  tc filter add dev $dev parent ffff: protocol all u32 match u32 0 0 action mirred egress redirect dev $ifb
  tc qdisc add dev $ifb root handle 1: htb default 10
  tc class add dev $ifb parent 1: classid 1:10 htb rate $taxa ceil $taxa
  tc qdisc add dev $ifb parent 1:10 handle 10: netem delay $atraso limit 10000
}
perfil eth1 20mbit 10ms     # matriz <-> filial 1: 20 Mbit/s, RTT 20 ms
perfil eth2 10mbit 30ms     # matriz <-> filial 2: 10 Mbit/s, RTT 60 ms
echo PROVEDOR_OK
'''
PROVEDOR_IF = '''auto eth0
iface eth0 inet static
\taddress 172.16.0.1
\tnetmask 255.255.255.252
auto eth1
iface eth1 inet static
\taddress 172.16.0.5
\tnetmask 255.255.255.252
auto eth2
iface eth2 inet static
\taddress 172.16.0.9
\tnetmask 255.255.255.252
auto eth3
iface eth3 inet dhcp
'''

PHP_SEM_NAT = r'''<?php
require_once '/usr/local/opnsense/mvc/script/load_phalcon.php';
$cfg = OPNsense\Core\Config::getInstance();
$o = $cfg->object();
if (!isset($o->nat)) { $o->addChild('nat'); }
if (!isset($o->nat->outbound)) { $o->nat->addChild('outbound'); }
if (isset($o->nat->outbound->mode)) { $o->nat->outbound->mode = 'disabled'; } else { $o->nat->outbound->addChild('mode', 'disabled'); }
$cfg->save();
echo "SEM_NAT_OK\n";
'''

# ------------------------------------------------------------------ 1) projeto e nós
for pr in g.api('GET', '/projects'):
    if pr['status'] == 'opened' and pr['name'] != 'TCC-etapa-0':
        x = g.Projeto(pr['name']); x.parar(); x.fechar(); log('fechado:', pr['name'])
p = g.Projeto('TCC-etapa-0', recriar=True)
N = {}
N['PROVEDOR'] = p.de_template('TCC - Provedor', 'PROVEDOR', 100, -470)
N['INTERNET'] = g.api('POST', f'/projects/{p.id}/nodes', {'name': 'INTERNET', 'node_type': 'nat', 'compute_id': g.COMPUTE, 'x': 330, 'y': -560})
pos = {'HQ': -450, 'F1': 100, 'F2': 400}
for s, c in SITES.items():
    x = pos[s]
    N[c['r']] = p.de_template('TCC - IOL L3 15.4', c['r'], x, -320)
    N[c['fw']] = p.de_template('TCC - OPNsense 26.7', c['fw'], x, -190)
N['SW-CORE'] = p.de_template('TCC - IOL L2 17.15', 'SW-CORE', -450, -40, symbol=':/symbols/classic/multilayer_switch.svg')
N['SW-ACC1'] = p.de_template('TCC - IOL L2 17.15', 'SW-ACC1', -630, 120)
N['SW-ACC2'] = p.de_template('TCC - IOL L2 17.15', 'SW-ACC2', -310, 120)
N['SW-FIL1'] = p.de_template('TCC - IOL L2 17.15', 'SW-FIL1', 100, -40)
N['SW-FIL2'] = p.de_template('TCC - IOL L2 17.15', 'SW-FIL2', 400, -40)
SERVICOS = {'APLICACAO': 'web ssh', 'ARQUIVOS': 'smb ssh'}   # servidores: imagem tcc-servidor:1 (decisão de 13/11)
for h, (ip, gw, sw, porta, x, y, sym) in HOSTS.items():
    iface = f'auto eth0\niface eth0 inet static\n\taddress {ip}\n\tnetmask 255.255.255.0\n\tgateway {gw}\n'
    N[h] = p.servidor_t(h, iface, SERVICOS[h], x, y, symbol=sym) if h in SERVICOS else p.host_t(h, iface, x, y, symbol=sym)
N['GERENCIA'] = g.api('POST', f'/projects/{p.id}/nodes', {'name': 'GERENCIA-WINDOWS', 'node_type': 'cloud', 'compute_id': g.COMPUTE,
    'x': -150, 'y': -470, 'properties': {'ports_mapping': [{'interface': 'eth0', 'name': 'eth0', 'port_number': 0, 'type': 'ethernet'}]}})
N['MGMT-SW'] = g.api('POST', f'/projects/{p.id}/nodes', {'name': 'MGMT-SW', 'node_type': 'ethernet_switch', 'compute_id': g.COMPUTE, 'x': -150, 'y': -380})
g.api('POST', f"/projects/{p.id}/nodes/{N['PROVEDOR']['node_id']}/files/etc/network/interfaces", bruto=PROVEDOR_IF)
log(f'{len(N)} nós criados a partir dos templates')

# ------------------------------------------------------------------ 2) cabos
L = [('PROVEDOR', (0, 0), 'R-HQ', (0, 0)), ('PROVEDOR', (1, 0), 'R-FIL1', (0, 0)), ('PROVEDOR', (2, 0), 'R-FIL2', (0, 0)),
     ('PROVEDOR', (3, 0), 'INTERNET', (0, 0)),
     ('R-HQ', (0, 1), 'FW-HQ', (1, 0)), ('R-FIL1', (0, 1), 'FW-F1', (1, 0)), ('R-FIL2', (0, 1), 'FW-F2', (1, 0)),
     ('FW-HQ', (0, 0), 'SW-CORE', (0, 0)), ('SW-CORE', (0, 1), 'SW-ACC1', (0, 0)), ('SW-CORE', (0, 2), 'SW-ACC2', (0, 0)),
     ('FW-F1', (0, 0), 'SW-FIL1', (0, 0)), ('FW-F2', (0, 0), 'SW-FIL2', (0, 0)),
     ('GERENCIA', (0, 0), 'MGMT-SW', (0, 0)), ('FW-HQ', (2, 0), 'MGMT-SW', (0, 1)), ('FW-F1', (2, 0), 'MGMT-SW', (0, 2)),
     ('FW-F2', (2, 0), 'MGMT-SW', (0, 3))]
L += [(h, (0, 0), v[2], v[3]) for h, v in HOSTS.items()]
for a, pa, b, pb in L:
    p.link(N[a], pa, N[b], pb)
log(f'{len(L)} cabos ligados')
(ET / 'cabeamento.txt').write_text('\n'.join(f'{a} {pa} <-> {b} {pb}' for a, pa, b, pb in L), encoding='utf-8')

# ------------------------------------------------------------------ 3) ligar
p.iniciar()
log('todos os nós ligados; aguardando boot')
time.sleep(20)

# ------------------------------------------------------------------ 4) PROVEDOR
pv = g.conteiner(p, N['PROVEDOR'])
(ET / 'provedor.sh').write_text(PROVEDOR_SH, encoding='utf-8')
g.vm_stdin(f'docker exec -i {pv} sh -c "cat > /etc/network/provedor.sh; chmod +x /etc/network/provedor.sh"', PROVEDOR_SH)
log('PROVEDOR:', g.vm(f'docker exec {pv} sh /etc/network/provedor.sh').strip()[-80:])

# ------------------------------------------------------------------ 5) roteadores
# gerência por Telnet com senha nas etapas 0 e A (decisão de 13/11; na B1 vira SSH + AAA)
TELNET = f'''enable secret {g.SENHA_CISCO}
line vty 0 4
 password {g.SENHA_CISCO}
 login
 transport input telnet'''
GER_SW = {'SW-CORE': ('10.10.10.2', '10.10.10.1'), 'SW-ACC1': ('10.10.10.3', '10.10.10.1'), 'SW-ACC2': ('10.10.10.4', '10.10.10.1'),
          'SW-FIL1': ('10.20.10.2', '10.20.10.1'), 'SW-FIL2': ('10.30.10.2', '10.30.10.1')}
for s, c in SITES.items():
    con = g.Console(p, N[c['r']]); assert g.cisco_pronto(con), c['r']
    rede, mask = c['rede'].split('/')[0], '255.255.0.0'
    g.cisco_config(con, f'''
hostname {c['r']}
no ip domain-lookup
interface Ethernet0/0
 description PROVEDOR
 ip address {c['prov'][1]} 255.255.255.252
 no shutdown
interface Ethernet0/1
 description {c['fw']} WAN
 ip address {c['wan'][0]} 255.255.255.252
 no shutdown
ip route 0.0.0.0 0.0.0.0 {c['prov'][0]}
ip route {rede} {mask} {c['wan'][1]}
{TELNET}''')
    g.cisco_salvar(con)
    (ET / f"{c['r']}.cfg").write_text(g.cisco_show(con, 'show running-config', 6), encoding='utf-8')
    log(f"{c['r']}: configurado e salvo")

# ------------------------------------------------------------------ 6) switches (etapa 0: tudo na VLAN 1)
for sw in ('SW-CORE', 'SW-ACC1', 'SW-ACC2', 'SW-FIL1', 'SW-FIL2'):
    con = g.Console(p, N[sw]); assert g.cisco_pronto(con), sw
    g.cisco_config(con, f'''
hostname {sw}
no ip domain-lookup
spanning-tree mode rapid-pvst
interface Vlan1
 ip address {GER_SW[sw][0]} 255.255.255.0
 no shutdown
exit
ip default-gateway {GER_SW[sw][1]}
ip route 0.0.0.0 0.0.0.0 {GER_SW[sw][1]}
{TELNET}''')
    g.cisco_salvar(con)
    (ET / f'{sw}.cfg').write_text(g.cisco_show(con, 'show running-config', 6), encoding='utf-8')
    log(f'{sw}: configurado e salvo')

# ------------------------------------------------------------------ 7) firewalls OPNsense
chaves = json.loads(CHAVES.read_text()) if CHAVES.exists() else {}
for s, c in SITES.items():
    fw = c['fw']
    con = g.Console(p, N[fw])
    assert g.opn_menu(con, 600), f'{fw} sem menu'
    assert g.opn_atribuir(con, opcionais=('vtnet2',)), f'{fw} atribuição'
    assert g.opn_ip(con, 'LAN', c['lan'], 24), f'{fw} LAN'
    assert g.opn_ip(con, 'WAN', c['wan'][1], 30, c['wan'][0]), f'{fw} WAN'
    assert g.opn_ip(con, 'OPT1', c['mgmt'], 24), f'{fw} OPT1'
    assert g.opn_wan_sem_bloqueios(con), f'{fw} bloqueios WAN'
    assert g.opn_entrar_shell(con)
    key, secret = g.opn_criar_apikey(con)
    g.opn_enviar_arquivo(con, PHP_SEM_NAT, '/tmp/semnat.php')
    out = g.opn_shell(con, 'php /tmp/semnat.php; rm -f /tmp/semnat.php; configctl filter reload >/dev/null', 120)
    con.enviar('exit'); con.esperar([r'Enter an option:\s*$'], 30)
    chaves[f'etapa0-{fw}'] = {'url': f"https://{c['lan']}", 'mgmt': f"https://{c['mgmt']}", 'key': key, 'secret': secret}
    CHAVES.write_text(json.dumps(chaves, indent=1))
    api = g.OpnAPI(p, N[c['apih']], chaves[f'etapa0-{fw}'])
    for regra in (dict(interface='wan', source_net='any', description='Etapa 0: rede plana, WAN libera tudo'),
                  dict(interface='opt1', source_net='192.168.16.0/24', description='Gerencia a partir do Windows')):
        base = {'enabled': '1', 'action': 'pass', 'quick': '1', 'direction': 'in', 'ipprotocol': 'inet',
                'protocol': 'any', 'destination_net': 'any'}
        base.update(regra)
        r = api('POST', 'firewall/filter/add_rule', {'rule': base})
        assert r.get('result') == 'saved', f'{fw} regra: {r}'
    api('POST', 'firewall/filter/apply', {})
    api.backup(ET / f'{fw}.xml')
    log(f"{fw}: LAN {c['lan']}/24, WAN {c['wan'][1]}/30 (gw {c['wan'][0]}), gerência {c['mgmt']}; sem NAT; WAN libera tudo; backup salvo "
        f"({'NAT desligado' if 'SEM_NAT_OK' in out else 'ATENÇÃO NAT: ' + out[-80:]})")

# ------------------------------------------------------------------ 8) teste funcional: todos alcançam todos
log('teste funcional (rede plana: todos alcançam todos)')
ips = {h: v[0] for h, v in HOSTS.items()}
linhas = []
for origem in ('PC-USUARIO', 'HOST-INVADIDO', 'PC-FIL1', 'PC-FIL2'):
    co = g.conteiner(p, N[origem])
    for destino, ip in ips.items():
        if destino == origem: continue
        out = g.vm(f'docker exec {co} ping -c 3 -i 0.3 -W 3 {ip} | tail -2')
        m = re.search(r'([\d.]+)% packet loss', out); rtt = re.search(r'= [\d.]+/([\d.]+)/', out)
        linha = f"{origem:14s} -> {destino:14s} perda {m.group(1) if m else '?':>3}%  RTT médio {rtt.group(1) if rtt else '-'} ms"
        linhas.append(linha); log(linha)
(ET / 'teste_funcional.txt').write_text('\n'.join(linhas), encoding='utf-8')
log('etapa 0 montada; configurações em lab/etapa-0/')
