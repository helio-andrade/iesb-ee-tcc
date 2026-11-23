"""Funções comuns dos scripts do laboratório.

Fala com o controlador do GNS3 do Windows (o mesmo da interface gráfica), para que
tudo o que os scripts criam apareça ao vivo no GNS3 desktop. Os equipamentos rodam
na GNS3 VM (compute "vm"). Comandos nos contêineres usam SSH na VM (docker exec).

Credenciais:
- controlador local: lidas de %APPDATA%\\GNS3\\2.2\\gns3_server.ini (seção [Server]);
- GNS3 VM: usuário/senha padrão gns3/gns3 (ajuste VM_USER/VM_PASS se mudar).
"""
import base64, configparser, json, os, re, socket, time, urllib.error, urllib.request
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding='utf-8', errors='replace'); _sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

VM_HOST = os.environ.get('GNS3_VM_HOST', '192.168.16.130')
VM_USER, VM_PASS = 'gns3', 'gns3'
COMPUTE = 'vm'


def _controlador():
    ini = os.path.join(os.environ['APPDATA'], 'GNS3', '2.2', 'gns3_server.ini')
    cp = configparser.ConfigParser(); cp.read(ini, encoding='utf-8')
    s = cp['Server']
    base = f"{s.get('protocol', 'http')}://{s.get('host', '127.0.0.1')}:{s.get('port', '3080')}/v2"
    hdr = {'Content-Type': 'application/json'}
    if s.getboolean('auth', fallback=False):
        tok = base64.b64encode(f"{s.get('user')}:{s.get('password')}".encode()).decode()
        hdr['Authorization'] = 'Basic ' + tok
    return base, hdr


BASE, HDR = _controlador()


def api(metodo, caminho, dados=None, bruto=None, timeout=180):
    corpo = bruto.encode() if bruto is not None else (json.dumps(dados).encode() if dados is not None else None)
    r = urllib.request.Request(BASE + caminho, method=metodo, data=corpo, headers=HDR)
    try:
        with urllib.request.urlopen(r, timeout=timeout) as x:
            t = x.read(); return json.loads(t) if t else None
    except urllib.error.HTTPError as e:
        raise RuntimeError(f'{metodo} {caminho}: {e.code} {e.read().decode()[:400]}')


class Projeto:
    """Projeto no controlador do Windows. Reabre se já existir com o mesmo nome."""

    def __init__(self, nome, recriar=False):
        existentes = {p['name']: p for p in api('GET', '/projects')}
        if nome in existentes and recriar:
            api('DELETE', f"/projects/{existentes[nome]['project_id']}")
            existentes.pop(nome)
        if nome in existentes:
            self.id = existentes[nome]['project_id']
            api('POST', f'/projects/{self.id}/open', {})
        else:
            self.id = api('POST', '/projects', {'name': nome})['project_id']
        self.nome = nome
        self._x = 0

    def _pos(self, x, y):
        if x is None:
            x, self._x = self._x, self._x + 150
        return x, (0 if y is None else y)

    def no(self, nome, tipo, props, x=None, y=None, symbol=None):
        x, y = self._pos(x, y)
        d = {'name': nome, 'node_type': tipo, 'compute_id': COMPUTE, 'properties': props, 'x': x, 'y': y}
        if symbol: d['symbol'] = symbol
        return api('POST', f'/projects/{self.id}/nodes', d)

    def de_template(self, template, nome, x=None, y=None, symbol=None, **props):
        """Cria um nó a partir de um template da interface do GNS3 (ex.: 'TCC - OPNsense 26.7')."""
        tid = next(t['template_id'] for t in api('GET', '/templates') if t['name'] == template)
        x, y = self._pos(x, y)
        n = api('POST', f'/projects/{self.id}/templates/{tid}', {'x': x, 'y': y, 'compute_id': COMPUTE})
        upd = {'name': nome}
        if symbol: upd['symbol'] = symbol
        if props: upd['properties'] = props
        return api('PUT', f"/projects/{self.id}/nodes/{n['node_id']}", upd)

    def host_t(self, nome, interfaces, x=None, y=None, symbol=None):
        """Host de teste a partir do template 'TCC - Host', com /etc/network/interfaces."""
        n = self.de_template('TCC - Host', nome, x, y, symbol)
        api('POST', f"/projects/{self.id}/nodes/{n['node_id']}/files/etc/network/interfaces", bruto=interfaces)
        return n

    def servidor_t(self, nome, interfaces, servicos, x=None, y=None, symbol=None):
        """Servidor a partir do template 'TCC - Servidor' (imagem tcc-servidor:1). servicos: ex. 'web ssh' ou 'smb ssh'."""
        n = self.de_template('TCC - Servidor', nome, x, y, symbol, environment=f'SERVICOS={servicos}')
        api('POST', f"/projects/{self.id}/nodes/{n['node_id']}/files/etc/network/interfaces", bruto=interfaces)
        return n

    def host(self, nome, interfaces, imagem='tcc-host:2', x=None, y=None):
        n = self.no(nome, 'docker', {'image': imagem, 'adapters': 1, 'console_type': 'telnet'}, x, y)
        api('POST', f"/projects/{self.id}/nodes/{n['node_id']}/files/etc/network/interfaces", bruto=interfaces)
        return n

    def iol(self, nome, imagem, ram=512, x=None, y=None):
        return self.no(nome, 'iou', {'path': imagem, 'ram': ram, 'nvram': 256}, x, y)

    def opnsense(self, nome, x=None, y=None, adaptadores=4):
        return self.no(nome, 'qemu', {
            # hda_disk_interface é obrigatório pela API: sem ele o disco fica "if=none" e a VM liga sem disco
            'hda_disk_image': 'OPNsense-24.7-nano-amd64.img', 'hda_disk_interface': 'virtio',
            'ram': 1536, 'cpus': 2, 'adapters': adaptadores,
            'adapter_type': 'virtio-net-pci', 'console_type': 'telnet', 'options': '-cpu host', 'platform': 'x86_64'}, x, y)

    def link(self, a, porta_a, b, porta_b):
        """porta = (adaptador, porta). IOL: e0/1 = (0, 1); QEMU/Docker: (n, 0)."""
        return api('POST', f'/projects/{self.id}/links', {'nodes': [
            {'node_id': a['node_id'], 'adapter_number': porta_a[0], 'port_number': porta_a[1]},
            {'node_id': b['node_id'], 'adapter_number': porta_b[0], 'port_number': porta_b[1]}]})

    def iniciar(self, n=None):
        api('POST', f'/projects/{self.id}/nodes/{n["node_id"]}/start' if n else f'/projects/{self.id}/nodes/start', {})

    def parar(self, n=None):
        api('POST', f'/projects/{self.id}/nodes/{n["node_id"]}/stop' if n else f'/projects/{self.id}/nodes/stop', {})

    def info(self, n):
        return api('GET', f"/projects/{self.id}/nodes/{n['node_id']}")

    def fechar(self):
        api('POST', f'/projects/{self.id}/close', {})


class Console:
    """Console telnet de um nó (o mesmo que a interface abre com duplo clique)."""

    def __init__(self, projeto, n):
        i = projeto.info(n)
        host = i.get('console_host') or VM_HOST
        if host in ('0.0.0.0', '::'):
            host = VM_HOST
        self.s = socket.create_connection((host, i['console']), timeout=5)
        self.s.settimeout(0.5); self.buf = ''

    def _ler(self, t):
        fim = time.time() + t
        while time.time() < fim:
            try:
                c = self.s.recv(65536)
                if c: self.buf += c.decode(errors='replace').replace('\r', '')
            except socket.timeout:
                pass

    def esperar(self, padroes, t):
        fim = time.time() + t
        while time.time() < fim:
            self._ler(0.5)
            for i, p in enumerate(padroes):
                m = re.search(p, self.buf)
                if m:
                    saida = self.buf[:m.end()]; self.buf = self.buf[m.end():]
                    return i, saida
        return -1, self.buf

    def enviar(self, texto, espera=0.0):
        self.s.sendall(texto.encode() + b'\r')
        if espera: self._ler(espera)


# ---------------------------------------------------------------- Cisco IOL (console)

SENHA_CISCO = 'tcc@2026'   # senha de laboratório (enable secret e vty a partir da etapa 0 com Telnet)


def cisco_pronto(con, t=300):
    """Espera o prompt do IOS, responde 'no' ao diálogo inicial e entra em modo privilegiado
    (responde à senha do enable, se houver enable secret)."""
    fim = time.time() + t
    while time.time() < fim:
        con.enviar('', 2)
        if 'initial configuration dialog' in con.buf[-400:]:
            con.enviar('no', 5)
        if re.search(r'\n\S+[>#]\s*$', con.buf):
            con.enviar('end', 1); con.buf = ''; con.enviar('enable', 1.5)
            if 'Password:' in con.buf[-60:]:
                con.enviar(SENHA_CISCO, 1.5)
            con.enviar('terminal length 0', 1)
            return True
    return False


def cisco_config(con, texto, espera=0.4):
    """Envia um bloco de configuração (uma linha por vez) a partir do modo privilegiado."""
    con.enviar('configure terminal', 1)
    for linha in texto.strip().splitlines():
        con.enviar(linha.rstrip(), espera)
    con.enviar('end', 1)


def cisco_show(con, cmd, t=4):
    con.buf = ''
    con.enviar(cmd, t)
    return con.buf


def cisco_salvar(con):
    """write memory (grava na NVRAM do nó; vai junto quando o projeto é duplicado)."""
    con.buf = ''
    con.enviar('write memory', 4)
    if '[confirm]' in con.buf:      # IOS-XE (IOL L2): "NVRAM ... written by a different version ... Overwrite?[confirm]"
        con.enviar('', 6)
    return 'OK' in con.buf[-300:] or '[OK]' in con.buf


_ssh = None


def vm(cmd, timeout=180):
    """Executa um comando na GNS3 VM por SSH e devolve stdout+stderr."""
    global _ssh
    import paramiko
    if _ssh is None:
        _ssh = paramiko.SSHClient(); _ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        _ssh.connect(VM_HOST, username=VM_USER, password=VM_PASS, look_for_keys=False, allow_agent=False)
    _, o, e = _ssh.exec_command(cmd, timeout=timeout)
    return o.read().decode() + e.read().decode()


def vm_stdin(cmd, dados, timeout=120):
    """Executa um comando na VM enviando 'dados' pela entrada padrão."""
    vm('true')
    i, o, e = _ssh.exec_command(cmd, timeout=timeout)
    i.write(dados); i.channel.shutdown_write()
    return o.read().decode() + e.read().decode()


class OpnAPI:
    """API do OPNsense chamada de dentro de um host da LAN (curl no contêiner), sem precisar
    de acesso do Windows à rede do laboratório. 'cred' = {'url','key','secret'}."""

    def __init__(self, projeto, host_no, cred):
        self.c = conteiner(projeto, host_no); self.cred = cred

    def __call__(self, metodo, caminho, dados=None):
        url = f"{self.cred['url']}/api/{caminho}"
        auth = f"{self.cred['key']}:{self.cred['secret']}"
        if dados is None:
            out = vm(f"docker exec {self.c} curl -sk -m 60 -u '{auth}' -X {metodo} '{url}'")
        else:
            out = vm_stdin(f"docker exec -i {self.c} curl -sk -m 60 -u '{auth}' -X {metodo} "
                           f"-H 'Content-Type: application/json' --data @- '{url}'", json.dumps(dados))
        try:
            return json.loads(out)
        except ValueError:
            return {'_bruto': out[:500]}

    def texto(self, caminho):
        """GET que devolve o corpo bruto (ex.: core/backup/download/this -> config.xml)."""
        auth = f"{self.cred['key']}:{self.cred['secret']}"
        return vm(f"docker exec {self.c} curl -sk -m 60 -u '{auth}' '{self.cred['url']}/api/{caminho}'")

    def backup(self, destino):
        """Salva o config.xml atual do firewall (System > Configuration > Backups) em 'destino'."""
        xml = self.texto('core/backup/download/this')
        if '<opnsense>' not in xml:
            raise RuntimeError('backup falhou: ' + xml[:200])
        pathlib_dest = __import__('pathlib').Path(destino)
        pathlib_dest.parent.mkdir(parents=True, exist_ok=True)
        pathlib_dest.write_text(xml, encoding='utf-8')
        return len(xml)


class OpnAPIGer:
    """API do OPNsense chamada do Windows pela rede de gerência (cred['mgmt'], ex. https://192.168.16.31).
    Não depende do endereço da LAN, que muda entre as etapas."""

    def __init__(self, cred):
        import ssl, base64
        self.url = cred['mgmt']; self.ctx = ssl._create_unverified_context()
        self.auth = 'Basic ' + base64.b64encode(f"{cred['key']}:{cred['secret']}".encode()).decode()

    def __call__(self, metodo, caminho, dados=None, timeout=60):
        import urllib.request
        h = {'Authorization': self.auth}
        if dados is not None:
            h['Content-Type'] = 'application/json'
        req = urllib.request.Request(f'{self.url}/api/{caminho}', method=metodo, headers=h,
                                     data=None if dados is None else json.dumps(dados).encode())
        corpo = urllib.request.urlopen(req, context=self.ctx, timeout=timeout).read().decode(errors='replace')
        try:
            return json.loads(corpo)
        except ValueError:
            return {'_bruto': corpo}

    def backup(self, destino):
        xml = self('GET', 'core/backup/download/this').get('_bruto', '')
        if '<opnsense>' not in xml:
            raise RuntimeError('backup falhou: ' + xml[:200])
        p = __import__('pathlib').Path(destino); p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(xml, encoding='utf-8')
        return len(xml)

    def regra(self, interface, origem, destino, descricao):
        r = self('POST', 'firewall/filter/add_rule', {'rule': {
            'enabled': '1', 'action': 'pass', 'quick': '1', 'direction': 'in', 'ipprotocol': 'inet', 'protocol': 'any',
            'interface': interface, 'source_net': origem, 'destination_net': destino, 'description': descricao}})
        assert r.get('result') == 'saved', r
        return r['uuid']

    def apagar_regras(self, trecho):
        """Apaga as regras cuja descrição contém 'trecho'; devolve quantas."""
        n = 0
        for r in self('GET', 'firewall/filter/search_rule').get('rows', []):
            if trecho in (r.get('description') or ''):
                self('POST', f"firewall/filter/del_rule/{r['uuid']}", {}); n += 1
        return n


def conteiner(projeto, n):
    """ID do contêiner Docker de um nó do GNS3 (informado pelo próprio GNS3)."""
    return projeto.info(n)['properties']['container_id']


# ---------------------------------------------------------------- OPNsense (console serial)

def opn_menu(con, t=600):
    """Garante login e volta ao menu principal ('Enter an option:')."""
    con.enviar('')
    for _ in range(20):
        k, out = con.esperar([r'login:\s*$', r'Password:\s*$', r'Enter an option:\s*$', r'\n>\s*$',
                              r'\[[yY]/[nN]\]\s*:?\s*$', r'#\s*$'], t)
        if k == 0: con.enviar('root')
        elif k == 1: con.enviar('opnsense')
        elif k == 2: return True
        elif k in (3, 4): con.enviar('n' if k == 4 else '')   # diálogo pendente: aceita padrão até sair
        elif k == 5: con.enviar('exit')                         # estava no shell: volta ao menu
        else: return False
        t = 60
    return False


def opn_shell(con, cmd, t=120):
    """Executa um comando no shell do OPNsense (menu opção 8) e devolve a saída.
    Entra no shell se estiver no menu; usa um marcador para saber onde a saída termina."""
    import shlex
    n = int(time.time() * 1000) % 100000
    marca = f'__FIM{n}__'                      # o que o echo imprime
    digitado = f'__FIM""{n}__'                 # o que aparece no eco do comando (diferente da marca)
    con.buf = ''
    con.enviar(f'sh -c {shlex.quote(cmd)}; echo {digitado}')
    k, out = con.esperar([r'(?m)^' + re.escape(marca) + r'\s*$'], t)
    linhas = out.splitlines()
    linhas = [l for l in linhas if digitado not in l and marca not in l]
    return '\n'.join(linhas).strip()


def opn_enviar_arquivo(con, conteudo, destino, pedaco=180):
    """Grava um arquivo no OPNsense pelo console serial, em pedaços curtos (o tty corta linhas longas)."""
    b64 = base64.b64encode(conteudo.encode()).decode()
    opn_shell(con, f'rm -f {destino}.b64')
    for i in range(0, len(b64), pedaco):
        opn_shell(con, f"printf %s {b64[i:i+pedaco]} >> {destino}.b64")
    opn_shell(con, f'b64decode -r < {destino}.b64 > {destino} && rm -f {destino}.b64')


PHP_APIKEY = r'''<?php
require_once '/usr/local/opnsense/mvc/script/load_phalcon.php';
$mdl = new OPNsense\Auth\User();
$r = null;
foreach ($mdl->user->iterateItems() as $node) {
    if ((string)$node->name == 'root') { $r = $node->apikeys->add(); }
}
$mdl->serializeToConfig(false, true);
OPNsense\Core\Config::getInstance()->save();
echo "APIKEY=" . $r['key'] . "\n";
echo "APISECRET=" . $r['secret'] . "\n";
'''


def opn_criar_apikey(con):
    """Gera uma chave de API para o root (precisa estar no shell). Devolve (key, secret)."""
    opn_enviar_arquivo(con, PHP_APIKEY, '/tmp/apikey.php')
    out = opn_shell(con, 'php /tmp/apikey.php; rm -f /tmp/apikey.php', 120)
    k = re.search(r'APIKEY=(\S+)', out); s = re.search(r'APISECRET=(\S+)', out)
    if not (k and s):
        raise RuntimeError('chave de API não gerada: ' + out[-300:])
    return k.group(1), s.group(1)


PHP_WAN_SEM_BLOQUEIOS = r'''<?php
require_once '/usr/local/opnsense/mvc/script/load_phalcon.php';
$cfg = OPNsense\Core\Config::getInstance();
$o = $cfg->object();
unset($o->interfaces->wan->blockpriv);
unset($o->interfaces->wan->blockbogons);
$cfg->save();
echo "WAN_SEM_BLOQUEIOS_OK\n";
'''


def opn_wan_sem_bloqueios(con):
    """Desliga 'Block private networks' e 'Block bogon networks' na WAN (laboratório usa IPs privados na WAN).
    Precisa ser refeito depois de qualquer reatribuição de interfaces (menu 1), que os religa."""
    assert opn_entrar_shell(con)
    opn_enviar_arquivo(con, PHP_WAN_SEM_BLOQUEIOS, '/tmp/wan.php')
    out = opn_shell(con, 'php /tmp/wan.php; rm -f /tmp/wan.php; configctl filter reload >/dev/null', 120)
    con.enviar('exit'); con.esperar([r'Enter an option:\s*$'], 30)
    return 'WAN_SEM_BLOQUEIOS_OK' in out


def opn_entrar_shell(con):
    assert opn_menu(con)
    con.enviar('8')
    k, _ = con.esperar([r'#\s*$'], 30)
    return k == 0


def opn_atribuir(con, wan='vtnet1', lan='vtnet0', opcionais=()):
    """Menu 1 do OPNsense: atribui interfaces (sem LAGG/VLAN). opcionais = ('vtnet2', ...) viram OPT1, OPT2..."""
    assert opn_menu(con)
    con.enviar('1')
    fila = list(opcionais)
    for _ in range(30):
        k, out = con.esperar([r'Enter an option:\s*$', r'\n>\s*$', r'\[[yY]/[nN]\]\s*:?\s*$', r':\s*$'], 180)
        if k == -1: return False
        if k == 0: return True
        q = out[-500:].lower()
        if 'lagg' in q or 'vlan' in q: con.enviar('n')
        elif 'wan interface name' in q: con.enviar(wan)
        elif 'lan interface name' in q: con.enviar(lan)
        elif 'optional interface' in q: con.enviar(fila.pop(0) if fila else '')
        elif 'proceed' in q: con.enviar('y')
        elif k == 2: con.enviar('n')
        else: con.enviar('')
    return False


def opn_ip(con, iface, ip, bits, gateway=''):
    """Menu 2 do OPNsense: IPv4 estático numa interface (LAN/WAN/OPTx), sem DHCP, sem IPv6."""
    assert opn_menu(con)
    con.enviar('2')
    for _ in range(30):
        k, out = con.esperar([r'Enter an option:\s*$', r'\n>\s*$', r'\[[yY]/[nN]\]\s*:?\s*$', r':\s*$'], 120)
        if k == -1:
            return False
        if k == 0:
            return True
        q = out[-400:].lower()
        if 'number of the interface' in q:
            m = re.search(r'(\d+)\s*-\s*' + re.escape(iface.lower()), q); con.enviar(m.group(1) if m else '')
        elif 'via dhcp6' in q or 'dhcp6' in q and '?' in q: con.enviar('n')
        elif 'via dhcp' in q: con.enviar('n')
        elif 'ipv4 address' in q and 'new' in q: con.enviar(ip)
        elif 'subnet bit count' in q and 'ipv6' not in q: con.enviar(str(bits))
        elif 'default' in q and 'gateway' in q and 'ipv6' not in q and k == 2: con.enviar('y' if gateway else 'n')
        elif 'upstream gateway' in q and 'ipv6' not in q: con.enviar(gateway)
        elif 'ipv6' in q: con.enviar('')
        elif k == 2: con.enviar('n')
        else: con.enviar('')
    return False
