"""Fase 6 (e conferência parcial) — estatística das baterias de ensaio.

Uso: python analisar.py [etapa ...]      (sem argumentos: todas as etapas em lab/dados/ensaios/etapa-*)
     python analisar.py --comparar 0 A   (teste t de Welch: etapa A em relação à etapa 0)
Para cada etapa, caminho, teste e tamanho: n, média, desvio-padrão, p95 e intervalo de confiança de 95% (t de Student)
das métricas; CPU média de cada equipamento por teste. Grava lab/dados/analise/<etapa>_desempenho.csv,
<etapa>_cpu.csv e um resumo legível <etapa>_resumo.md.

--comparar: para cada caminho/teste/tamanho/métrica (e a CPU de cada equipamento), diferença das médias (B − A),
IC 95% da diferença, t e graus de liberdade de Welch-Satterthwaite, p bicaudal e p ajustado por Holm-Bonferroni
(muitas comparações ao mesmo tempo). Grava comparacao_<A>_vs_<B>.csv e .md em lab/dados/analise/.
Sem dependências externas: a distribuição t é calculada pela função beta incompleta regularizada.
"""
import csv, math, pathlib, statistics, sys
from collections import defaultdict

RAIZ = pathlib.Path(__file__).resolve().parents[1]
ENS = RAIZ / 'dados' / 'ensaios'
OUT = RAIZ / 'dados' / 'analise'; OUT.mkdir(parents=True, exist_ok=True)
# t de Student bicaudal 95% para n-1 graus de liberdade (n até 31); acima disso ~1,96
T95 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228,
       11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131, 16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086,
       21: 2.080, 22: 2.074, 23: 2.069, 24: 2.064, 25: 2.060, 26: 2.056, 27: 2.052, 28: 2.048, 29: 2.045, 30: 2.042}
METRICAS = {'latencia': ['rtt_medio_ms', 'rtt_p95_ms', 'perda_pct'], 'tcp': ['vazao_mbps', 'retrans'],
            'udp': ['vazao_mbps', 'jitter_ms', 'perda_pct']}


def estat(v):
    v = [x for x in v if x is not None]
    n = len(v)
    if n == 0:
        return dict(n=0)
    m = statistics.mean(v)
    dp = statistics.stdev(v) if n > 1 else 0.0
    ic = (T95.get(n - 1, 1.96) * dp / math.sqrt(n)) if n > 1 else 0.0
    vs = sorted(v)
    p95 = vs[max(0, math.ceil(0.95 * n) - 1)]
    return dict(n=n, media=m, dp=dp, p95=p95, ic95=ic)


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def analisar(pasta):
    etapa = pasta.name
    grupos = defaultdict(lambda: defaultdict(list))
    with open(pasta / 'resultados.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            k = (r['caminho'], r['teste'], r['tamanho_bytes'])
            for mt in METRICAS[r['teste']]:
                grupos[k][mt].append(num(r[mt]))
    linhas_md = [f'# Resumo — {etapa}', '', '| caminho | teste | tamanho (B) | métrica | n | média | dp | p95 | IC 95% (±) |', '|---|---|---|---|---|---|---|---|---|']
    with open(OUT / f'{etapa}_desempenho.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['etapa', 'caminho', 'teste', 'tamanho_bytes', 'metrica', 'n', 'media', 'dp', 'p95', 'ic95'])
        for (cam, teste, tam), mets in sorted(grupos.items()):
            for mt, vals in mets.items():
                e = estat(vals)
                if not e['n']:
                    continue
                w.writerow([etapa, cam, teste, tam, mt, e['n'], f"{e['media']:.3f}", f"{e['dp']:.3f}", f"{e['p95']:.3f}", f"{e['ic95']:.3f}"])
                linhas_md.append(f"| {cam} | {teste} | {tam or '—'} | {mt} | {e['n']} | {e['media']:.2f} | {e['dp']:.2f} | {e['p95']:.2f} | {e['ic95']:.2f} |")
    cpu = defaultdict(list)
    if (pasta / 'cpu.csv').exists():
        with open(pasta / 'cpu.csv', encoding='utf-8') as f:
            for r in csv.DictReader(f):
                cpu[(r['caminho'], r['teste'], r['tamanho_bytes'], r['equipamento'])].append(num(r['cpu_pct_1nucleo']))
    with open(OUT / f'{etapa}_cpu.csv', 'w', newline='', encoding='utf-8') as f:
        # mediana além da média: tarefas periódicas do OPNsense geram picos isolados que puxam a média
        w = csv.writer(f); w.writerow(['etapa', 'caminho', 'teste', 'tamanho_bytes', 'equipamento', 'n', 'cpu_media', 'cpu_ic95', 'cpu_mediana'])
        for k, vals in sorted(cpu.items()):
            e = estat(vals)
            if e['n']:
                med = statistics.median([x for x in vals if x is not None])
                w.writerow([etapa, *k, e['n'], f"{e['media']:.1f}", f"{e['ic95']:.1f}", f"{med:.1f}"])
    (OUT / f'{etapa}_resumo.md').write_text('\n'.join(linhas_md), encoding='utf-8')
    print(f'{etapa}: {len(grupos)} grupos -> {OUT}')


# ---------- comparação entre etapas: teste t de Welch ----------

def _betacf(a, b, x):
    """Fração continuada da beta incompleta (Numerical Recipes, betacf)."""
    MAXIT, EPS, FPMIN = 300, 3e-14, 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    d = 1.0 / (d if abs(d) > FPMIN else FPMIN)
    h = d
    for m in range(1, MAXIT + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d; d = 1.0 / (d if abs(d) > FPMIN else FPMIN)
        c = 1.0 + aa / c; c = c if abs(c) > FPMIN else FPMIN
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d; d = 1.0 / (d if abs(d) > FPMIN else FPMIN)
        c = 1.0 + aa / c; c = c if abs(c) > FPMIN else FPMIN
        de = d * c; h *= de
        if abs(de - 1.0) < EPS:
            break
    return h


def _ibeta(a, b, x):
    """Beta incompleta regularizada I_x(a, b)."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    ln = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x)
    if x < (a + 1) / (a + b + 2):
        return math.exp(ln) * _betacf(a, b, x) / a
    return 1.0 - math.exp(ln) * _betacf(b, a, 1 - x) / b


def p_bicaudal(t, gl):
    """P(|T| > |t|) para T ~ t de Student com gl graus de liberdade."""
    return _ibeta(gl / 2.0, 0.5, gl / (gl + t * t))


def t_critico(gl, alfa=0.05):
    """Quantil bicaudal da t (bissecção sobre p_bicaudal)."""
    lo, hi = 0.0, 1000.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if p_bicaudal(mid, gl) > alfa:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def welch(a, b):
    """Teste t de Welch (B − A). Devolve dict com diferença, IC 95%, t, gl e p; None se não der para testar."""
    a = [x for x in a if x is not None]; b = [x for x in b if x is not None]
    na, nb = len(a), len(b)
    if na < 2 or nb < 2:
        return None
    ma, mb = statistics.mean(a), statistics.mean(b)
    va, vb = statistics.variance(a), statistics.variance(b)
    se2 = va / na + vb / nb
    dif = mb - ma
    if se2 == 0:   # as duas amostras sem variação: diferença exata
        return dict(na=na, nb=nb, media_a=ma, media_b=mb, dif=dif, ic_inf=dif, ic_sup=dif, t=None, gl=None,
                    p=0.0 if dif else 1.0)
    se = math.sqrt(se2)
    gl = se2 ** 2 / ((va / na) ** 2 / (na - 1) + (vb / nb) ** 2 / (nb - 1))
    t = dif / se
    tc = t_critico(gl)
    return dict(na=na, nb=nb, media_a=ma, media_b=mb, dif=dif, ic_inf=dif - tc * se, ic_sup=dif + tc * se,
                t=t, gl=gl, p=p_bicaudal(t, gl))


def holm(ps):
    """p ajustados por Holm-Bonferroni (mesma ordem da entrada)."""
    m = len(ps)
    ordem = sorted(range(m), key=lambda i: ps[i])
    aj, maior = [0.0] * m, 0.0
    for k, i in enumerate(ordem):
        maior = max(maior, min(1.0, (m - k) * ps[i]))
        aj[i] = maior
    return aj


def _amostras(pasta):
    g = defaultdict(list)
    with open(pasta / 'resultados.csv', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            for mt in METRICAS[r['teste']]:
                g[(r['caminho'], r['teste'], r['tamanho_bytes'], mt)].append(num(r[mt]))
    if (pasta / 'cpu.csv').exists():
        with open(pasta / 'cpu.csv', encoding='utf-8') as f:
            for r in csv.DictReader(f):
                g[(r['caminho'], r['teste'], r['tamanho_bytes'], 'cpu_pct:' + r['equipamento'])].append(num(r['cpu_pct_1nucleo']))
    return g


def comparar(ea, eb):
    na_, nb_ = (e if e.startswith('etapa-') else f'etapa-{e}' for e in (ea, eb))
    A, B = _amostras(ENS / na_), _amostras(ENS / nb_)
    linhas = []
    for k in sorted(set(A) & set(B)):
        w = welch(A[k], B[k])
        if w:
            linhas.append((k, w))
    pa = holm([w['p'] for _, w in linhas])
    nome = f'comparacao_{na_}_vs_{nb_}'
    f8 = lambda x: '' if x is None else f'{x:.4g}'
    md = [f'# {nb_} em relação a {na_} (teste t de Welch, IC 95%, p ajustado por Holm)', '',
          '| caminho | teste | tamanho (B) | métrica | média A | média B | diferença | dif. % | IC 95% da diferença | p (Holm) | significativa |',
          '|---|---|---|---|---|---|---|---|---|---|---|']
    with open(OUT / f'{nome}.csv', 'w', newline='', encoding='utf-8') as f:
        wr = csv.writer(f)
        wr.writerow(['caminho', 'teste', 'tamanho_bytes', 'metrica', 'n_a', 'n_b', 'media_a', 'media_b', 'diferenca',
                     'diferenca_pct', 'ic95_inf', 'ic95_sup', 't', 'gl', 'p', 'p_holm', 'significativa_5pct'])
        for ((cam, teste, tam, mt), w), ph in zip(linhas, pa):
            pct = (w['dif'] / w['media_a'] * 100) if w['media_a'] else None
            sig = 'sim' if ph < 0.05 else 'não'
            wr.writerow([cam, teste, tam, mt, w['na'], w['nb'], f8(w['media_a']), f8(w['media_b']), f8(w['dif']),
                         f8(pct), f8(w['ic_inf']), f8(w['ic_sup']), f8(w['t']), f8(w['gl']), f8(w['p']), f8(ph), sig])
            if not mt.startswith('cpu_pct:'):
                md.append(f"| {cam} | {teste} | {tam or '—'} | {mt} | {w['media_a']:.3g} | {w['media_b']:.3g} | "
                          f"{w['dif']:+.3g} | {'' if pct is None else f'{pct:+.1f}%'} | [{w['ic_inf']:.3g}; {w['ic_sup']:.3g}] | "
                          f"{ph:.3g} | {sig} |")
    (OUT / f'{nome}.md').write_text('\n'.join(md), encoding='utf-8')
    nsig = sum(1 for p in pa if p < 0.05)
    print(f'{nome}: {len(linhas)} comparações, {nsig} significativas (Holm, 5%) -> {OUT}')


if __name__ == '__main__':
    if len(sys.argv) == 4 and sys.argv[1] == '--comparar':
        comparar(sys.argv[2], sys.argv[3])
        sys.exit()
    alvos =[ENS / (a if a.startswith('etapa-') else f'etapa-{a}') for a in sys.argv[1:]] or sorted(p for p in ENS.glob('etapa-*') if p.is_dir())
    for pasta in alvos:
        if (pasta / 'resultados.csv').exists():
            analisar(pasta)
