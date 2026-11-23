"""Gerência por Telnet com senha nos Cisco da etapa 0 (decisão de 13/11: Telnet nas etapas 0 e A; SSH + AAA na B1).

Uso: python gerencia_telnet_etapa0.py [TCC-etapa-0]
- Roteadores: enable secret + line vty com senha, só Telnet. Alcançáveis pelos IPs que já têm.
- Switches: o mesmo + IP de gerência na VLAN 1 (rede plana) e default-gateway.
Grava (write memory) e exporta o running-config para lab/<etapa>/<nome>.cfg.
Não digite nos consoles enquanto o script roda.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import gns3lab as g

PROJ = sys.argv[1] if len(sys.argv) > 1 else 'TCC-etapa-0'
PASTA = pathlib.Path(__file__).resolve().parents[1] / PROJ.replace('TCC-', '').lower()
S = g.SENHA_CISCO
COMUM = f"""
enable secret {S}
line vty 0 4
 password {S}
 login
 transport input telnet
"""
SWITCHES = {'SW-CORE': ('10.10.10.2', '10.10.10.1'), 'SW-ACC1': ('10.10.10.3', '10.10.10.1'), 'SW-ACC2': ('10.10.10.4', '10.10.10.1'),
            'SW-FIL1': ('10.20.10.2', '10.20.10.1'), 'SW-FIL2': ('10.30.10.2', '10.30.10.1')}
ROTEADORES = ['R-HQ', 'R-FIL1', 'R-FIL2']

p = g.Projeto(PROJ)
nos = {n['name']: n for n in g.api('GET', f'/projects/{p.id}/nodes')}
for nome in ROTEADORES + list(SWITCHES):
    con = g.Console(p, nos[nome])
    if not g.cisco_pronto(con, 60):
        print(nome, 'sem prompt'); continue
    cfg = COMUM
    if nome in SWITCHES:
        ip, gw = SWITCHES[nome]
        # o IOL L2 vem com "ip routing" ligado: o default-gateway é ignorado, é preciso rota padrão estática
        cfg += f"interface Vlan1\n ip address {ip} 255.255.255.0\n no shutdown\nexit\nip default-gateway {gw}\nip route 0.0.0.0 0.0.0.0 {gw}\n"
    g.cisco_config(con, cfg)
    ok = g.cisco_salvar(con)
    run = g.cisco_show(con, 'show running-config', 6)
    txt = run[run.find('Building configuration'):] if 'Building configuration' in run else run
    (PASTA / f'{nome}.cfg').write_text(txt, encoding='utf-8')
    print(f"{nome}: telnet {'ok' if 'transport input telnet' in run else 'FALHOU'}, gravado {ok}"
          + (f", gerência {SWITCHES[nome][0]}" if nome in SWITCHES else ''))
