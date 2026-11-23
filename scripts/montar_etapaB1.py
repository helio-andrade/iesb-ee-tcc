"""Etapa B1 — Zero Trust, a partir do TCC-etapa-B1 (duplicado do TCC-etapa-A, ligado).

Uso: python montar_etapaB1.py [passo ...]     (sem argumentos: todos, na ordem)
Passos: radius enclave fwhq portal filiais acl gerencia l2 backup teste

Controles (NIST SP 800-207; enclave = seção 3.2.2):
  radius   FreeRADIUS no FW-HQ (plugin instalado antes, à mão: pkg install os-freeradius): usuário do portal e
           usuário de gerência; clientes: o próprio OPNsense (portal) e os switches da matriz (AAA)
  enclave  VLAN 20 (servidores) passa a ter o FW-HQ como gateway (10.10.20.1, VLAN etiquetada no trunk do SW-CORE)
  fwhq     bloqueio padrão no FW-HQ: só fluxos explícitos (usuário → serviços dos servidores, medição, RADIUS, relay)
  portal   portal cativo no FW-HQ (interface de trânsito) autenticando no FreeRADIUS
  filiais  bloqueio padrão nos firewalls das filiais: só a medição (matriz → filial, filial 1 → filial 2)
  acl      ACL na SVI da VLAN 10 do SW-CORE: usuários não alcançam a gerência nem as SVIs do switch
  gerencia SSH + AAA (RADIUS nos switches da matriz, local nos demais); vty só a partir da gerência
  l2       DAI com ligações estáticas e port security nas portas dos hosts
  backup   config.xml dos firewalls e running-config dos Cisco em lab/etapa-B1/
  teste    teste funcional (fluxos permitidos e bloqueados)
Não digite nos consoles enquanto o script roda.
"""
import json, pathlib, re, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import gns3lab as g

def log(*a): print(time.strftime('%H:%M:%S'), *a, flush=True)
RAIZ = pathlib.Path(__file__).resolve().parents[1]
ET = RAIZ / 'etapa-B1'; ET.mkdir(exist_ok=True)
CHAVES = json.loads((RAIZ / 'dados' / 'opnsense_api_keys.json').read_text())
p = g.Projeto('TCC-etapa-B1')
N = {n['name']: n for n in g.api('GET', f'/projects/{p.id}/nodes')}
FW = {fw: g.OpnAPIGer(CHAVES[f'etapa0-{fw}']) for fw in ('FW-HQ', 'FW-F1', 'FW-F2')}
hq = FW['FW-HQ']
PORTAL_USUARIO, PORTAL_SENHA = 'usuario1', 'Senha.Tcc1'
GER_USUARIO, GER_SENHA = 'admin-rede', 'Rede.Tcc1'
SEG_LOCAL, SEG_SW = 'tcc-portal-2026', 'tcc-radius-sw'
IP = {'PC-USUARIO': '10.10.10.11', 'HOST-INVADIDO': '10.10.10.12', 'APLICACAO': '10.10.20.21', 'ARQUIVOS': '10.10.20.22',
      'PC-FIL1': '10.20.10.11', 'PC-FIL2': '10.30.10.11'}


def ok(r, oque):
    assert isinstance(r, dict) and (r.get('result') in ('saved', 'ok') or r.get('status') in ('ok', 'OK')), f'{oque}: {r}'


def shell_fw(fw, cmd, t=120):
    con = g.Console(p, N[fw]); assert g.opn_entrar_shell(con)
    out = g.opn_shell(con, cmd, t)
    con.enviar('exit'); return out


def php_fw(fw, codigo, t=120):
    con = g.Console(p, N[fw]); assert g.opn_entrar_shell(con)
    g.opn_enviar_arquivo(con, codigo, '/tmp/b1.php')
    out = g.opn_shell(con, 'php /tmp/b1.php; rm -f /tmp/b1.php', t)
    con.enviar('exit'); return out


def alias(api, nome, tipo, conteudo, descr):
    if any(a.get('name') == nome for a in api('GET', 'firewall/alias/search_item').get('rows', [])):
        return
    ok(api('POST', 'firewall/alias/add_item', {'alias': {'enabled': '1', 'name': nome, 'type': tipo,
                                                         'content': '\n'.join(conteudo), 'description': descr}}), f'alias {nome}')


def regra(api, interface, proto, origem, destino, porta, descr):
    ok(api('POST', 'firewall/filter/add_rule', {'rule': {
        'enabled': '1', 'action': 'pass', 'quick': '1', 'direction': 'in', 'ipprotocol': 'inet', 'protocol': proto,
        'interface': interface, 'source_net': origem, 'destination_net': destino, 'destination_port': porta,
        'description': 'Etapa B1: ' + descr}}), descr)


PHP_PADRAO_NEGA = r'''<?php
require_once '/usr/local/opnsense/mvc/script/load_phalcon.php';
$cfg = OPNsense\Core\Config::getInstance(); $o = $cfg->object();
$n = 0;
foreach ($o->filter->rule as $r) { if (strpos((string)$r->descr, 'Default allow LAN') === 0) { $r->disabled = '1'; $n++; } }
$o->system->webgui->noantilockout = '1';
$cfg->save();
echo "NEGA_OK $n\n";
'''

PHP_AUTHSERVER = r'''<?php
require_once '/usr/local/opnsense/mvc/script/load_phalcon.php';
$cfg = OPNsense\Core\Config::getInstance(); $o = $cfg->object();
foreach ($o->system->authserver as $a) { if ((string)$a->name == 'FreeRADIUS-local') { echo "AUTHSERVER_OK\n"; exit; } }
$a = $o->system->addChild('authserver');
$a->addChild('refid', uniqid()); $a->addChild('type', 'radius'); $a->addChild('name', 'FreeRADIUS-local');
$a->addChild('host', '127.0.0.1'); $a->addChild('radius_secret', '%SEG%'); $a->addChild('radius_timeout', '5');
$a->addChild('radius_srvcs', 'both'); $a->addChild('radius_auth_port', '1812'); $a->addChild('radius_acct_port', '1813');
$a->addChild('radius_protocol', 'PAP');
$cfg->save(); echo "AUTHSERVER_OK\n";
'''.replace('%SEG%', SEG_LOCAL)

PHP_IF_SERVIDORES = r'''<?php
require_once '/usr/local/opnsense/mvc/script/load_phalcon.php';
$cfg = OPNsense\Core\Config::getInstance(); $o = $cfg->object();
$i = isset($o->interfaces->opt2) ? $o->interfaces->opt2 : $o->interfaces->addChild('opt2');
$i->if = '%DEV%'; $i->descr = 'SERVIDORES'; $i->enable = '1'; $i->ipaddr = '10.10.20.1'; $i->subnet = '24';
$cfg->save(); echo "IF_OK\n";
'''


# ------------------------------------------------------------------ passos
def passo_radius():
    ok(hq('POST', 'freeradius/general/set', {'general': {'enabled': '1', 'log_authentication_request': '1'}}), 'radius geral')
    clientes = {c.get('name') for c in hq('GET', 'freeradius/client/search_client').get('rows', [])}
    for nome, ip, seg in (('OPNsense-local', '127.0.0.1', SEG_LOCAL), ('SW-CORE', '10.10.100.2', SEG_SW),
                          ('SW-ACC1', '10.10.99.3', SEG_SW), ('SW-ACC2', '10.10.99.4', SEG_SW)):
        if nome not in clientes:
            ok(hq('POST', 'freeradius/client/add_client', {'client': {'enabled': '1', 'name': nome, 'secret': seg, 'ip': ip}}), nome)
    usuarios = {u.get('username') for u in hq('GET', 'freeradius/user/search_user').get('rows', [])}
    for u, s in ((PORTAL_USUARIO, PORTAL_SENHA), (GER_USUARIO, GER_SENHA)):
        if u not in usuarios:
            ok(hq('POST', 'freeradius/user/add_user', {'user': {'enabled': '1', 'username': u, 'password': s}}), u)
    hq('POST', 'freeradius/service/reconfigure', {})
    out = php_fw('FW-HQ', PHP_AUTHSERVER)
    log('FreeRADIUS: clientes (local, SW-CORE, SW-ACC1, SW-ACC2), usuários', PORTAL_USUARIO, GER_USUARIO,
        '| servidor de autenticação:', 'ok' if 'AUTHSERVER_OK' in out else out[-120:])


def passo_enclave():
    # 1) dispositivo VLAN 20 sobre a vtnet0 (mesmo cabo do trunk)
    vlans = hq('GET', 'interfaces/vlan_settings/search_item').get('rows', [])
    if not any(str(v.get('tag')) == '20' for v in vlans):
        ok(hq('POST', 'interfaces/vlan_settings/add_item', {'vlan': {'if': 'vtnet0', 'tag': '20', 'pcp': '0', 'descr': 'SERVIDORES'}}), 'vlan 20')
        hq('POST', 'interfaces/vlan_settings/reconfigure', {})
    dev = next(v['vlanif'] for v in hq('GET', 'interfaces/vlan_settings/search_item')['rows'] if str(v.get('tag')) == '20')
    # 2) SW-CORE: sai a SVI da VLAN 20; a VLAN 20 passa etiquetada no trunk até o FW-HQ
    con = g.Console(p, N['SW-CORE']); assert g.cisco_pronto(con, 60)
    g.cisco_config(con, 'no interface Vlan20\ninterface Ethernet0/0\n switchport trunk allowed vlan add 20', 0.8)
    assert g.cisco_salvar(con)
    # 3) FW-HQ: interface SERVIDORES (opt2) = 10.10.20.1/24 na VLAN 20
    out = php_fw('FW-HQ', PHP_IF_SERVIDORES.replace('%DEV%', dev))
    for h in ('APLICACAO', 'ARQUIVOS'):
        g.vm(f'docker exec {g.conteiner(p, N[h])} ip neigh flush all')
    # verificação a partir do firewall: a interface dos servidores já nasce em bloqueio padrão (o servidor não pinga o FW)
    out2 = shell_fw('FW-HQ', 'configctl interface reconfigure opt2; configctl filter reload; sleep 2; '
                             f'ping -c 3 -t 4 {IP["APLICACAO"]} | tail -1; ping -c 3 -t 4 {IP["ARQUIVOS"]} | tail -1', 180)
    log(f'enclave: VLAN 20 ({dev}) no FW-HQ ->', 'ok' if 'IF_OK' in out else out[-100:], '| FW-HQ -> servidores:', out2.strip()[-140:])


def passo_fwhq():
    hq_ = hq
    n = hq_.apagar_regras('Etapa A') + hq_.apagar_regras('Etapa B1')
    alias(hq_, 'P_APLICACAO', 'port', ['80', '443', '5201'], 'HTTP, HTTPS e medição (iperf3)')
    alias(hq_, 'PCS_FILIAIS', 'host', [IP['PC-FIL1'], IP['PC-FIL2']], 'hosts de medição das filiais')
    alias(hq_, 'GER_MATRIZ', 'network', ['10.10.100.2/32', '10.10.99.0/24'], 'gerência da matriz (switches)')
    hq_('POST', 'firewall/alias/reconfigure', {})
    u = IP['PC-USUARIO']
    regra(hq_, 'lan', 'TCP', u, IP['APLICACAO'], 'P_APLICACAO', 'usuário -> aplicação (HTTP, HTTPS, medição)')
    regra(hq_, 'lan', 'UDP', u, IP['APLICACAO'], '5201', 'usuário -> aplicação (medição UDP)')
    regra(hq_, 'lan', 'ICMP', u, IP['APLICACAO'], '', 'usuário -> aplicação (latência)')
    regra(hq_, 'lan', 'TCP', u, IP['ARQUIVOS'], '445', 'usuário -> arquivos (SMB)')
    regra(hq_, 'lan', 'TCP/UDP', u, 'PCS_FILIAIS', '5201', 'usuário -> filiais (medição)')
    regra(hq_, 'lan', 'ICMP', u, 'PCS_FILIAIS', '', 'usuário -> filiais (latência)')
    regra(hq_, 'lan', 'UDP', 'GER_MATRIZ', '10.10.100.1', '1812', 'switches da matriz -> RADIUS (AAA)')
    # o IOS envia o pedido retransmitido com origem = giaddr = IP da SVI do cliente (10.10.10.1), não o da interface de trânsito;
    # a regra antiga (origem 10.10.100.2) deixava a VLAN 10 sem DHCP (corrigido em 14/11, ver diário)
    regra(hq_, 'lan', 'UDP', '10.10.10.1', '10.10.100.1', '67', 'relay DHCP da VLAN 10 (origem = giaddr 10.10.10.1)')
    padrao = hq_.apagar_regras('Default allow LAN')        # regra 'rede da LAN -> qualquer' (IPv4 e IPv6)
    out = php_fw('FW-HQ', PHP_PADRAO_NEGA)
    hq_('POST', 'firewall/filter/apply', {})
    log(f'FW-HQ: {padrao} regra(s) padrão "LAN -> qualquer" removida(s)')
    log(f'FW-HQ: {n} regra(s) antiga(s) removida(s); 8 regras explícitas; regras padrão da LAN e anti-lockout desligados ->',
        out.strip().splitlines()[-1] if out.strip() else '?')


def passo_portal():
    if not hq('GET', 'captiveportal/settings/search_zones').get('rows'):
        ok(hq('POST', 'captiveportal/settings/add_zone', {'zone': {
            'enabled': '1', 'interfaces': 'lan', 'authservers': 'FreeRADIUS-local', 'idletimeout': '0', 'hardtimeout': '0',
            'concurrentlogins': '1', 'allowedAddresses': '10.10.100.2,10.10.10.1,10.10.99.0/24', 'description': 'Etapa B1: acesso ao enclave'}}), 'zona')
    hq('POST', 'captiveportal/service/reconfigure', {})
    time.sleep(8)
    log('portal cativo: zona na interface de trânsito (lan), FreeRADIUS-local; SW-CORE e gerência liberados')


def teste_portal():
    c = g.conteiner(p, N['PC-USUARIO']); inv = g.conteiner(p, N['HOST-INVADIDO'])
    web = lambda co: g.vm(f"docker exec {co} curl -s -m 6 -o /dev/null -w '%{{http_code}}' http://{IP['APLICACAO']}/").strip() or 'sem resposta'
    url = 'http://10.10.100.1:8000/api/captiveportal/access/logon/0'
    login = lambda co, s: g.vm(f"docker exec {co} curl -s -m 15 -w ' tempo=%{{time_total}}s' -X POST -d 'user={PORTAL_USUARIO}&password={s}' {url}").strip()
    r = {'sem login (HTTP)': web(c), 'senha errada': login(c, 'errada'), 'depois da senha errada (HTTP)': web(c),
         'senha certa': login(c, PORTAL_SENHA), 'depois do login (HTTP)': web(c),
         'host invadido, sem login (HTTP)': web(inv)}
    for k, v in r.items():
        log(f'portal | {k}: {v[:160]}')
    return r


def passo_filiais():
    f1, f2 = FW['FW-F1'], FW['FW-F2']
    for api in (f1, f2):
        api.apagar_regras('Etapa A'); api.apagar_regras('Etapa B1')
    # FW-F1: a matriz (PC-USUARIO) mede até o PC-FIL1; o PC-FIL1 mede até o PC-FIL2
    regra(f1, 'wan', 'TCP/UDP', IP['PC-USUARIO'], IP['PC-FIL1'], '5201', 'matriz -> PC-FIL1 (medição)')
    regra(f1, 'wan', 'ICMP', IP['PC-USUARIO'], IP['PC-FIL1'], '', 'matriz -> PC-FIL1 (latência)')
    regra(f1, 'lan', 'TCP/UDP', IP['PC-FIL1'], IP['PC-FIL2'], '5201', 'PC-FIL1 -> PC-FIL2 (medição)')
    regra(f1, 'lan', 'ICMP', IP['PC-FIL1'], IP['PC-FIL2'], '', 'PC-FIL1 -> PC-FIL2 (latência)')
    # FW-F2: recebe a medição da matriz e da filial 1
    alias(f2, 'ORIGENS_MED', 'host', [IP['PC-USUARIO'], IP['PC-FIL1']], 'origens da medição')
    f2('POST', 'firewall/alias/reconfigure', {})
    regra(f2, 'wan', 'TCP/UDP', 'ORIGENS_MED', IP['PC-FIL2'], '5201', 'matriz e filial 1 -> PC-FIL2 (medição)')
    regra(f2, 'wan', 'ICMP', 'ORIGENS_MED', IP['PC-FIL2'], '', 'matriz e filial 1 -> PC-FIL2 (latência)')
    for fw in ('FW-F1', 'FW-F2'):
        padrao = FW[fw].apagar_regras('Default allow LAN')
        log(f'{fw}: {padrao} regra(s) padrão "LAN -> qualquer" removida(s)')
        out = php_fw(fw, PHP_PADRAO_NEGA)
        FW[fw]('POST', 'firewall/filter/apply', {})
        log(f'{fw}: bloqueio padrão; só medição permitida ->', out.strip().splitlines()[-1] if out.strip() else '?')


def passo_acl():
    con = g.Console(p, N['SW-CORE']); assert g.cisco_pronto(con, 60)
    g.cisco_config(con, '''no ip access-list extended B1-USUARIOS
ip access-list extended B1-USUARIOS
 remark Etapa B1: usuarios nao alcancam a gerencia nem as SVIs do switch
 deny ip any 10.10.99.0 0.0.0.255
 deny tcp any host 10.10.10.1 eq 22
 deny tcp any host 10.10.10.1 eq 23
 deny tcp any host 10.10.100.2 eq 22
 deny tcp any host 10.10.100.2 eq 23
 permit ip any any
exit
interface Vlan10
 ip access-group B1-USUARIOS in''', 0.6)
    assert g.cisco_salvar(con)
    log('SW-CORE: ACL B1-USUARIOS na entrada da VLAN 10')


MATRIZ_SW = {'SW-CORE': 'Vlan100', 'SW-ACC1': 'Vlan99', 'SW-ACC2': 'Vlan99'}


def passo_gerencia():
    for nome in ('R-HQ', 'R-FIL1', 'R-FIL2', 'SW-CORE', 'SW-ACC1', 'SW-ACC2', 'SW-FIL1', 'SW-FIL2'):
        radius = nome in MATRIZ_SW
        metodo = 'group radius local' if radius else 'local'
        # IOS-XE (IOL L2) às vezes só aceita "ip domain name"; sem domínio, as chaves RSA (e o SSH) não são geradas
        cfg = f'''ip domain-name tcc.lab
ip domain name tcc.lab
username {GER_USUARIO} privilege 15 secret {GER_SENHA}
aaa new-model
aaa authentication login CONSOLE none
aaa authentication login VTY {metodo}
aaa authorization exec VTY local if-authenticated
{"radius server FWHQ" if radius else ""}
{" address ipv4 10.10.100.1 auth-port 1812 acct-port 1813" if radius else ""}
{" key " + SEG_SW if radius else ""}
{"exit" if radius else ""}
{"ip radius source-interface " + MATRIZ_SW[nome] if radius else ""}
no ip access-list standard GERENCIA
ip access-list standard GERENCIA
 permit 10.10.99.0 0.0.0.255
 permit 10.10.100.0 0.0.0.3
 permit 192.168.16.0 0.0.0.255
exit
ip ssh version 2
line con 0
 login authentication CONSOLE
line vty 0 4
 no password
 login authentication VTY
 authorization exec VTY
 transport input ssh
 access-class GERENCIA in'''
        con = g.Console(p, N[nome]); assert g.cisco_pronto(con, 60), nome
        g.cisco_config(con, '\n'.join(l for l in cfg.splitlines() if l.strip()), 0.6)
        con.enviar('configure terminal', 1); con.buf = ''
        con.enviar('crypto key generate rsa modulus 2048', 25)
        if 'yes/no' in con.buf[-200:]:
            con.enviar('yes', 25)
        con.enviar('end', 1)
        assert g.cisco_salvar(con), nome
        teste = ''
        if radius:
            teste = g.cisco_show(con, f'test aaa group radius {GER_USUARIO} {GER_SENHA} new-code', 12)
            teste = 'RADIUS ok' if 'successfully authenticated' in teste else 'RADIUS FALHOU: ' + teste.strip()[-120:]
        ssh = g.cisco_show(con, 'show ip ssh | include SSH', 4)
        log(f'{nome}: SSH + AAA ({metodo}); vty só da gerência; {"SSH ativo" if "Enabled" in ssh else "SSH?"} {teste}')


def mac_ios(mac):
    h = mac.replace(':', '').lower()
    return f'{h[0:4]}.{h[4:8]}.{h[8:12]}'


L2 = {'SW-ACC1': ('10', [('PC-USUARIO', 'Ethernet0/1'), ('HOST-INVADIDO', 'Ethernet0/2')]),
      'SW-ACC2': ('20', [('APLICACAO', 'Ethernet0/1'), ('ARQUIVOS', 'Ethernet0/2')]),
      'SW-FIL1': ('1', [('PC-FIL1', 'Ethernet0/1')]),
      'SW-FIL2': ('1', [('PC-FIL2', 'Ethernet0/1')])}


def passo_l2():
    for sw, (vlan, hosts) in L2.items():
        linhas = ['no arp access-list ARP-HOSTS', 'arp access-list ARP-HOSTS']
        portas = []
        for h, porta in hosts:
            mac = g.api('GET', f"/projects/{p.id}/nodes/{N[h]['node_id']}")['properties']['mac_address']
            linhas.append(f' permit ip host {IP[h]} mac host {mac_ios(mac)}')
            portas += [f'interface {porta}', ' switchport mode access', f' switchport access vlan {vlan}' if vlan != '1' else '',
                       ' switchport port-security', ' switchport port-security maximum 1',
                       f' switchport port-security mac-address {mac_ios(mac)}', ' switchport port-security violation restrict']
        linhas += ['exit', f'ip arp inspection filter ARP-HOSTS vlan {vlan} static', f'ip arp inspection vlan {vlan}',
                   'interface Ethernet0/0', ' ip arp inspection trust'] + portas
        con = g.Console(p, N[sw]); assert g.cisco_pronto(con, 60), sw
        g.cisco_config(con, '\n'.join(l for l in linhas if l.strip()), 0.6)
        assert g.cisco_salvar(con), sw
        log(f'{sw}: DAI (VLAN {vlan}, ligações estáticas) e port security em {", ".join(pt for _, pt in hosts)}')


def passo_backup():
    for fw, api in FW.items():
        api.backup(ET / f'{fw}.xml')
    for nome in ('R-HQ', 'R-FIL1', 'R-FIL2', 'SW-CORE', 'SW-ACC1', 'SW-ACC2', 'SW-FIL1', 'SW-FIL2'):
        con = g.Console(p, N[nome]); g.cisco_pronto(con, 60)
        run = g.cisco_show(con, 'show running-config', 8)
        (ET / f'{nome}.cfg').write_text(run[run.find('Building configuration'):] if 'Building configuration' in run else run, encoding='utf-8')
    log('backups em lab/etapa-B1/')


def passo_teste():
    co = {h: g.conteiner(p, N[h]) for h in IP}
    for h in ('APLICACAO', 'PC-FIL1', 'PC-FIL2'):
        g.vm(f'docker exec {co[h]} sh -c "killall iperf3 2>/dev/null; iperf3 -s -D"')
    teste_portal()                                   # deixa o PC-USUARIO autenticado
    def ping(o, d): return ' 0% packet loss' in g.vm(f"docker exec {co[o]} ping -c 3 -W 2 {IP[d] if d in IP else d} | grep loss")
    def web(o, d): return 'Aplicacao interna' in g.vm(f"docker exec {co[o]} curl -s -m 6 http://{IP[d]}/")
    def tcp(o, d, pt): return 'ABERTO' in g.vm(f"docker exec {co[o]} sh -c 'nc -z -w 3 {IP[d] if d in IP else d} {pt} && echo ABERTO'")
    casos = [  # (descrição, função, esperado)
        ('PC-USUARIO -> APLICACAO (ping)', lambda: ping('PC-USUARIO', 'APLICACAO'), True),
        ('PC-USUARIO -> APLICACAO (página web)', lambda: web('PC-USUARIO', 'APLICACAO'), True),
        ('PC-USUARIO -> ARQUIVOS :445', lambda: tcp('PC-USUARIO', 'ARQUIVOS', 445), True),
        ('PC-USUARIO -> PC-FIL1 (ping)', lambda: ping('PC-USUARIO', 'PC-FIL1'), True),
        ('PC-USUARIO -> PC-FIL2 (ping)', lambda: ping('PC-USUARIO', 'PC-FIL2'), True),
        ('PC-USUARIO -> PC-FIL1 :5201', lambda: tcp('PC-USUARIO', 'PC-FIL1', 5201), True),
        ('PC-FIL1 -> PC-FIL2 (ping)', lambda: ping('PC-FIL1', 'PC-FIL2'), True),
        ('PC-FIL1 -> PC-FIL2 :5201', lambda: tcp('PC-FIL1', 'PC-FIL2', 5201), True),
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
    (ET / 'teste_funcional.txt').write_text('\n'.join(linhas), encoding='utf-8')
    log(f'teste funcional: {len(casos) - falhas}/{len(casos)} conforme a política')


PASSOS = {'radius': passo_radius, 'enclave': passo_enclave, 'fwhq': passo_fwhq, 'portal': passo_portal, 'teste_portal': teste_portal,
          'filiais': passo_filiais, 'acl': passo_acl, 'gerencia': passo_gerencia, 'l2': passo_l2, 'backup': passo_backup,
          'teste': passo_teste}
if __name__ == '__main__':
    for nome in (sys.argv[1:] or list(PASSOS)):
        PASSOS[nome]()
