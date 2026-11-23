"""Custo no plano de controle da etapa B1: tempo de autenticação no portal cativo (login -> FreeRADIUS -> liberação).

Uso: python medir_portal.py --projeto TCC-etapa-B1 --etapa B1 [--repeticoes 30]
Em cada repetição, a partir do PC-USUARIO: logoff; login com senha errada (recusa); login correto; primeiro acesso HTTP
ao servidor da aplicação. Os tempos são os do curl (time_total), medidos no próprio PC, sem o atraso do comando remoto.
Saída: lab/dados/ensaios/etapa-<etapa>/portal.csv. Ao final o PC fica autenticado (estado em que o ensaio roda).
"""
import argparse, csv, json, pathlib, re, statistics as st, sys, time
import gns3lab as g

ap = argparse.ArgumentParser()
ap.add_argument('--projeto', required=True); ap.add_argument('--etapa', required=True)
ap.add_argument('--repeticoes', type=int, default=30)
ap.add_argument('--usuario', default='usuario1'); ap.add_argument('--senha', default='Senha.Tcc1')
A = ap.parse_args()

PORTAL = 'http://10.10.100.1:8000/api/captiveportal/access'
SERVIDOR = 'http://10.10.20.21/'
SAIDA = pathlib.Path(__file__).resolve().parent.parent / 'dados' / 'ensaios' / f'etapa-{A.etapa}' / 'portal.csv'

p = g.Projeto(A.projeto)
nos = {n['name']: n for n in g.api('GET', f'/projects/{p.id}/nodes')}
c = g.conteiner(p, nos['PC-USUARIO'])


def curl(args):
    """Devolve (corpo, código HTTP, tempo em ms)."""
    r = g.vm(f"docker exec {c} curl -s -m 15 -w '\\n@@%{{http_code}} %{{time_total}}' {args}", 40)
    corpo, _, fim = r.rpartition('@@')
    cod, t = fim.split()
    return corpo, cod, float(t) * 1000


def autorizado(corpo):
    return 'AUTHORIZED' in corpo.replace('NOT_AUTHORIZED', '')


linhas = []
for rep in range(1, A.repeticoes + 1):
    corpo_off, _, _ = curl(f"-X POST -d '' {PORTAL}/logoff/0")              # POST sem corpo: 411 (a sessão continuaria)
    if 'AUTHORIZED' in corpo_off.replace('NOT_AUTHORIZED', ''):
        raise SystemExit(f'logoff não encerrou a sessão: {corpo_off[:200]}')
    time.sleep(1)
    _, cod_bloq, _ = curl(f'-o /dev/null {SERVIDOR}')                         # sem sessão: redirecionado (302)
    corpo_err, _, t_err = curl(f"-X POST -d 'user={A.usuario}&password=errada' {PORTAL}/logon/0")
    corpo, _, t_login = curl(f"-X POST -d 'user={A.usuario}&password={A.senha}' {PORTAL}/logon/0")
    _, cod_ok, t_http = curl(f'-o /dev/null {SERVIDOR}')                      # primeiro acesso já autorizado
    linhas.append({'etapa': A.etapa, 'rep': rep, 'data_hora': time.strftime('%Y-%m-%dT%H:%M:%S'),
                   'http_sem_sessao': cod_bloq, 'recusa_senha_errada': 'sim' if not autorizado(corpo_err) else 'nao',
                   't_senha_errada_ms': round(t_err, 1), 'login_ok': 'sim' if autorizado(corpo) else 'nao',
                   't_login_ms': round(t_login, 1), 'http_apos_login': cod_ok, 't_primeiro_acesso_ms': round(t_http, 1)})
    print(f"{rep:2d}: sem sessão {cod_bloq} | senha errada {t_err:6.1f} ms | login {t_login:6.1f} ms "
          f"({linhas[-1]['login_ok']}) | 1º acesso {cod_ok} em {t_http:5.1f} ms", flush=True)

SAIDA.parent.mkdir(parents=True, exist_ok=True)
with SAIDA.open('w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(linhas[0])); w.writeheader(); w.writerows(linhas)


def resumo(campo):
    v = [l[campo] for l in linhas]
    return f'média {st.mean(v):.1f} ms, mediana {st.median(v):.1f}, dp {st.stdev(v):.1f}, min {min(v):.1f}, máx {max(v):.1f}'


print('\nlogin correto:', resumo('t_login_ms'))
print('senha errada :', resumo('t_senha_errada_ms'))
print('1º acesso    :', resumo('t_primeiro_acesso_ms'))
print('bloqueado sem sessão:', sum(l['http_sem_sessao'] == '302' for l in linhas), '/', len(linhas),
      '| recusas corretas:', sum(l['recusa_senha_errada'] == 'sim' for l in linhas),
      '| logins ok:', sum(l['login_ok'] == 'sim' for l in linhas), '| 1º acesso 200:', sum(l['http_apos_login'] == '200' for l in linhas))
print('->', SAIDA)
