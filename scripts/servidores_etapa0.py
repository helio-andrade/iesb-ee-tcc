"""Troca APLICACAO e ARQUIVOS de um projeto pela imagem tcc-servidor:1 (template 'TCC - Servidor').

Uso: python servidores_etapa0.py [TCC-etapa-0]
A imagem de um nó Docker não pode ser trocada pela API do GNS3; o nó é substituído por um novo com o mesmo nome,
posição, símbolo, IP (/etc/network/interfaces) e porta no switch. Serviços (variável SERVICOS da imagem):
  APLICACAO: web (HTTP 80, HTTPS 443, lighttpd) + ssh (OpenSSH)
  ARQUIVOS:  smb (Samba 139/445) + ssh
Credencial de laboratório nos dois: operador / tcc@2026.
"""
import sys, pathlib, time
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import gns3lab as g

PROJ = sys.argv[1] if len(sys.argv) > 1 else 'TCC-etapa-0'
SERVIDORES = {'APLICACAO': ('10.10.10.21', 'web ssh'), 'ARQUIVOS': ('10.10.10.22', 'smb ssh')}

p = g.Projeto(PROJ)
nos = {n['name']: n for n in g.api('GET', f'/projects/{p.id}/nodes')}
links = g.api('GET', f'/projects/{p.id}/links')
for nome, (ip, servicos) in SERVIDORES.items():
    velho = nos[nome]
    if g.api('GET', f"/projects/{p.id}/nodes/{velho['node_id']}")['properties'].get('image') == 'tcc-servidor:1':
        print(nome, 'já usa tcc-servidor:1')
        continue
    # ligação atual: (nó vizinho, adaptador, porta) e a porta do próprio servidor
    lk = next(l for l in links if any(e['node_id'] == velho['node_id'] for e in l['nodes']))
    meu = next(e for e in lk['nodes'] if e['node_id'] == velho['node_id'])
    viz = next(e for e in lk['nodes'] if e['node_id'] != velho['node_id'])
    x, y, sym = velho['x'], velho['y'], velho.get('symbol')
    g.api('POST', f"/projects/{p.id}/nodes/{velho['node_id']}/stop")
    g.api('DELETE', f"/projects/{p.id}/links/{lk['link_id']}")
    g.api('DELETE', f"/projects/{p.id}/nodes/{velho['node_id']}")
    iface = f'auto eth0\niface eth0 inet static\n\taddress {ip}\n\tnetmask 255.255.255.0\n\tgateway 10.10.10.1\n'
    novo = p.servidor_t(nome, iface, servicos, x, y, symbol=sym)
    p.link(novo, (meu['adapter_number'], meu['port_number']), {'node_id': viz['node_id']}, (viz['adapter_number'], viz['port_number']))
    p.iniciar(novo)
    print(f'{nome}: substituído (tcc-servidor:1, SERVICOS={servicos}), ligado de volta em {viz["node_id"][:8]} {viz["adapter_number"]}/{viz["port_number"]}')
time.sleep(8)
nos = {n['name']: n for n in g.api('GET', f'/projects/{p.id}/nodes')}
for nome in SERVIDORES:
    c = g.conteiner(p, nos[nome])
    print(nome, nos[nome]['status'], g.vm(f'docker exec {c} sh -c "ip -4 -o addr show eth0 | awk \'{{print \\$4}}\'; netstat -tln | awk \'/LISTEN/ && \\$4 !~ /:::/{{print \\$4}}\' | tr \'\\n\' \' \'"'))
