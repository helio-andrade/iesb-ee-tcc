"""Conferência independente da estatística do analisar.py com a biblioteca scipy.

Uso: python lab/scripts/conferir_scipy.py            (todas as comparações em lab/dados/analise/comparacao_*.csv)
     python lab/scripts/conferir_scipy.py 0 A        (só a comparação da etapa A em relação à etapa 0)

O analisar.py calcula a distribuição t em Python puro (beta incompleta regularizada) e usa uma tabela t arredondada
nos intervalos de confiança de cada etapa. Este script refaz as contas com o scipy, a partir dos dados brutos, e
confere três coisas:
  1. Comparações entre etapas (teste t de Welch): para cada linha de comparacao_<A>_vs_<B>.csv, recalcula a diferença
     das médias (B − A), t, graus de liberdade de Welch-Satterthwaite, p bicaudal e IC 95% da diferença com
     scipy.stats.ttest_ind(B, A, equal_var=False), e o p ajustado por Holm-Bonferroni. Compara com os valores
     gravados no CSV (4 algarismos significativos) e com o welch() do analisar.py em precisão total.
  2. A decisão: se alguma diferença muda de "significativa" para "não significativa" (ou o contrário) no nível de 5%.
  3. Intervalos de confiança de cada etapa (<etapa>_desempenho.csv): IC 95% com o quantil exato da t do scipy,
     contra o da tabela arredondada do analisar.py.
A leitura dos dados brutos é feita aqui, com código próprio; do analisar.py só se importa o welch(), para comparar
as duas implementações em precisão total.
Saída: lab/dados/analise/conferencia_scipy.csv (uma linha por comparação) e conferencia_scipy.md (resumo).
"""
import csv, math, pathlib, re, statistics, sys, warnings
from collections import defaultdict

import scipy
from scipy import stats

# Em poucos grupos as repetições são quase idênticas (CPU praticamente constante); o scipy avisa que a variância
# perde precisão nesses casos. O resultado continua válido para a conferência: a decisão é comparada caso a caso.
warnings.filterwarnings('ignore', message='Precision loss occurred in moment calculation')

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = pathlib.Path(__file__).resolve().parent
LAB = AQUI.parent
ENS, ANA = LAB / 'dados' / 'ensaios', LAB / 'dados' / 'analise'
sys.path.insert(0, str(AQUI))
import analisar  # noqa: E402  (só o welch(), para a comparação em precisão total)

# as mesmas métricas registradas pelo ensaio.py
METRICAS = {'latencia': ['rtt_medio_ms', 'rtt_p95_ms', 'perda_pct'], 'tcp': ['vazao_mbps', 'retrans'],
            'udp': ['vazao_mbps', 'jitter_ms', 'perda_pct']}
ALFA = 0.05


def valor(x):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return v if math.isfinite(v) else None


def amostras(etapa):
    """Amostras de uma etapa: chave (caminho, teste, tamanho, métrica) -> lista de valores (sem vazios)."""
    pasta = ENS / etapa
    g = defaultdict(list)
    with open(pasta / 'resultados.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            for mt in METRICAS[r['teste']]:
                v = valor(r[mt])
                if v is not None:
                    g[(r['caminho'], r['teste'], r['tamanho_bytes'], mt)].append(v)
    if (pasta / 'cpu.csv').exists():
        with open(pasta / 'cpu.csv', encoding='utf-8') as f:
            for r in csv.DictReader(f):
                v = valor(r['cpu_pct_1nucleo'])
                if v is not None:
                    g[(r['caminho'], r['teste'], r['tamanho_bytes'], 'cpu_pct:' + r['equipamento'])].append(v)
    return g


def holm_scipy(ps):
    """Holm-Bonferroni escrito de outra forma (passo a passo descendente com máximo acumulado), para conferir."""
    m = len(ps)
    pares = sorted(enumerate(ps), key=lambda par: (par[1], par[0]))
    ajust, acumulado = {}, 0.0
    for posicao, (indice, p) in enumerate(pares, start=1):
        acumulado = max(acumulado, min(1.0, p * (m - posicao + 1)))
        ajust[indice] = acumulado
    return [ajust[i] for i in range(m)]


ZERO = 1e-9   # abaixo disso o valor é zero: médias iguais dão 0 exato no analisar.py e ~1e-15 (ruído) no scipy


def dif_rel(a, b):
    """Diferença relativa entre dois números (0 se ambos forem zero ou ausentes do mesmo jeito)."""
    if a is None or b is None:
        return 0.0 if a is None and b is None else math.inf
    if abs(a) < ZERO and abs(b) < ZERO:
        return 0.0
    escala = max(abs(a), abs(b))
    return abs(a - b) / escala


def conferir_comparacao(csv_cmp):
    m = re.fullmatch(r'comparacao_(etapa-.+)_vs_(etapa-.+)', csv_cmp.stem)
    ea, eb = m.group(1), m.group(2)
    A, B = amostras(ea), amostras(eb)
    linhas = list(csv.DictReader(open(csv_cmp, encoding='utf-8')))
    calc = []
    for r in linhas:
        k = (r['caminho'], r['teste'], r['tamanho_bytes'], r['metrica'])
        a, b = A[k], B[k]
        res = stats.ttest_ind(b, a, equal_var=False)          # B − A, como no analisar.py
        dif = statistics.fmean(b) - statistics.fmean(a)
        if math.isnan(res.statistic):                          # as duas amostras sem variação: diferença exata
            p, t, gl, ic = (0.0 if dif else 1.0), None, None, (dif, dif)
        else:
            ci = res.confidence_interval(1 - ALFA)
            p, t, gl, ic = float(res.pvalue), float(res.statistic), float(res.df), (float(ci.low), float(ci.high))
        w = analisar.welch(a, b)                               # implementação em Python puro, precisão total
        calc.append(dict(r=r, n=(len(a), len(b)), dif=dif, t=t, gl=gl, p=p, ic=ic, w=w))
    p_holm = holm_scipy([c['p'] for c in calc])
    maior = defaultdict(float)
    decisoes_diferentes = []
    for c, ph in zip(calc, p_holm):
        r, w = c['r'], c['w']
        # 1a. contra o CSV gravado (4 algarismos significativos)
        for nome, gravado, novo in (('diferenca', r['diferenca'], c['dif']), ('t', r['t'], c['t']), ('gl', r['gl'], c['gl']),
                                    ('p', r['p'], c['p']), ('p_holm', r['p_holm'], ph),
                                    ('ic95_inf', r['ic95_inf'], c['ic'][0]), ('ic95_sup', r['ic95_sup'], c['ic'][1])):
            maior['csv_' + nome] = max(maior['csv_' + nome], dif_rel(valor(gravado), novo))
        # 1b. contra o welch() do analisar.py, em precisão total (diferença absoluta no p)
        maior['puro_p_abs'] = max(maior['puro_p_abs'], abs(w['p'] - c['p']))
        if c['t'] is not None:
            maior['puro_t'] = max(maior['puro_t'], dif_rel(w['t'], c['t']))
            maior['puro_gl'] = max(maior['puro_gl'], dif_rel(w['gl'], c['gl']))
            maior['puro_ic'] = max(maior['puro_ic'], dif_rel(w['ic_inf'], c['ic'][0]), dif_rel(w['ic_sup'], c['ic'][1]))
        # 2. a decisão no nível de 5%
        sig_scipy = 'sim' if ph < ALFA else 'não'
        if sig_scipy != r['significativa_5pct']:
            decisoes_diferentes.append(f"{r['caminho']} / {r['teste']} {r['tamanho_bytes'] or ''} / {r['metrica']}: "
                                       f"gravado {r['significativa_5pct']}, scipy {sig_scipy} (p Holm {ph:.4g})")
    nsig = sum(1 for ph in p_holm if ph < ALFA)
    return dict(comparacao=f'{ea} vs {eb}', linhas=len(calc), significativas=nsig, decisoes_diferentes=decisoes_diferentes, **maior)


def conferir_ic_etapas():
    """IC 95% de cada etapa, recalculado dos dados brutos.

    Devolve: total de intervalos; maior diferença relativa entre o IC com a tabela t arredondada do analisar.py e com o
    quantil exato do scipy; quantos IC gravados no CSV fogem do esperado. O gravado tem duas fontes de arredondamento:
    3 casas decimais (até 5e-4 absoluto) e a tabela t (até ~2e-4 relativo, que pesa nos intervalos grandes).
    """
    total, pior_tabela, pior_gravado = 0, 0.0, 0
    for arq in sorted(ANA.glob('etapa-*_desempenho.csv')):
        etapa = arq.stem[:-len('_desempenho')]
        if not (ENS / etapa / 'resultados.csv').exists():
            continue
        brutos = amostras(etapa)
        for r in csv.DictReader(open(arq, encoding='utf-8')):
            v = brutos[(r['caminho'], r['teste'], r['tamanho_bytes'], r['metrica'])]
            n = len(v)
            if n < 2:
                continue
            dp = statistics.stdev(v)
            if dp == 0:
                continue
            ic_exato = stats.t.ppf(1 - ALFA / 2, n - 1) * dp / math.sqrt(n)
            ic_tabela = analisar.T95.get(n - 1, 1.96) * dp / math.sqrt(n)
            pior_tabela = max(pior_tabela, dif_rel(ic_tabela, ic_exato))
            tolerancia = 5e-4 + 3e-4 * ic_exato
            pior_gravado += abs(valor(r['ic95']) - ic_exato) > tolerancia
            total += 1
    return total, pior_tabela, pior_gravado


def main():
    if len(sys.argv) == 3:
        nomes = [f'etapa-{e}' if not e.startswith('etapa-') else e for e in sys.argv[1:]]
        arquivos = [ANA / f'comparacao_{nomes[0]}_vs_{nomes[1]}.csv']
    else:
        arquivos = sorted(ANA.glob('comparacao_*_vs_*.csv'))
    res = [conferir_comparacao(a) for a in arquivos]
    n_ic, pior_tabela, pior_gravado = conferir_ic_etapas()
    campos = ['comparacao', 'linhas', 'significativas', 'csv_diferenca', 'csv_t', 'csv_gl', 'csv_p', 'csv_p_holm',
              'csv_ic95_inf', 'csv_ic95_sup', 'puro_p_abs', 'puro_t', 'puro_gl', 'puro_ic', 'decisoes_diferentes']
    with open(ANA / 'conferencia_scipy.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(campos)
        for r in res:
            w.writerow([r['comparacao'], r['linhas'], r['significativas']] +
                       [f"{r.get(c, 0.0):.3g}" for c in campos[3:-1]] + [len(r['decisoes_diferentes'])])
    total = sum(r['linhas'] for r in res)
    mudancas = [d for r in res for d in r['decisoes_diferentes']]
    p_puro = max(r['puro_p_abs'] for r in res)
    csv_max = max(max(r[c] for c in campos[3:10]) for r in res)
    md = ['# Conferência da estatística com o scipy', '',
          f'scipy {scipy.__version__}, Python {sys.version.split()[0]}. Gerado por `lab/scripts/conferir_scipy.py`.', '',
          f'- **{len(res)} comparações entre etapas, {total} testes de Welch** refeitos com `scipy.stats.ttest_ind(B, A, equal_var=False)` a partir dos dados brutos.',
          f'- **Decisão (significativa ou não, Holm, 5%):** {"igual em todos os testes" if not mudancas else f"{len(mudancas)} diferença(s)"}.',
          f'- **Contra o `welch()` do analisar.py, em precisão total:** maior diferença absoluta no p = {p_puro:.2e}.',
          f'- **Contra os CSV gravados (4 algarismos significativos):** maior diferença relativa = {csv_max:.2e} (esperado: até ~5e-4, pelo arredondamento da gravação).',
          f'- **IC 95% de cada etapa ({n_ic} intervalos, recalculados dos dados brutos):** a tabela t arredondada do analisar.py '
          f'difere do quantil exato do scipy em no máximo {pior_tabela:.2e} (relativo); '
          f'IC gravados fora do esperado pelos arredondamentos (3 casas decimais e tabela t): {pior_gravado}.',
          '', '| comparação | testes | significativas | maior dif. relativa (CSV) | maior dif. no p (Python puro) | decisões diferentes |',
          '|---|---|---|---|---|---|']
    for r in res:
        md.append(f"| {r['comparacao']} | {r['linhas']} | {r['significativas']} | {max(r[c] for c in campos[3:10]):.2e} | "
                  f"{r['puro_p_abs']:.2e} | {len(r['decisoes_diferentes'])} |")
    if mudancas:
        md += ['', '## Decisões diferentes', ''] + [f'- {d}' for d in mudancas]
    (ANA / 'conferencia_scipy.md').write_text('\n'.join(md) + '\n', encoding='utf-8')
    print('\n'.join(md[:9]))
    print(f'\n-> {ANA / "conferencia_scipy.csv"} e conferencia_scipy.md')
    return 1 if mudancas else 0


if __name__ == '__main__':
    sys.exit(main())
