# Conferência da estatística com o scipy

scipy 1.18.1, Python 3.14.3. Gerado por `lab/scripts/conferir_scipy.py`.

- **9 comparações entre etapas, 3204 testes de Welch** refeitos com `scipy.stats.ttest_ind(B, A, equal_var=False)` a partir dos dados brutos.
- **Decisão (significativa ou não, Holm, 5%):** igual em todos os testes.
- **Contra o `welch()` do analisar.py, em precisão total:** maior diferença absoluta no p = 2.13e-12.
- **Contra os CSV gravados (4 algarismos significativos):** maior diferença relativa = 4.93e-04 (esperado: até ~5e-4, pelo arredondamento da gravação).
- **IC 95% de cada etapa (510 intervalos, recalculados dos dados brutos):** a tabela t arredondada do analisar.py difere do quantil exato do scipy em no máximo 2.29e-04 (relativo); IC gravados fora do esperado pelos arredondamentos (3 casas decimais e tabela t): 0.

| comparação | testes | significativas | maior dif. relativa (CSV) | maior dif. no p (Python puro) | decisões diferentes |
|---|---|---|---|---|---|
| etapa-0-rodada1 vs etapa-0 | 356 | 46 | 4.73e-04 | 2.84e-13 | 0 |
| etapa-0 vs etapa-0-verificacao | 356 | 3 | 4.80e-04 | 2.82e-13 | 0 |
| etapa-0 vs etapa-A | 356 | 54 | 4.93e-04 | 3.62e-13 | 0 |
| etapa-0 vs etapa-B1 | 356 | 123 | 4.80e-04 | 2.13e-12 | 0 |
| etapa-0 vs etapa-B2 | 356 | 138 | 4.64e-04 | 1.79e-13 | 0 |
| etapa-A vs etapa-B1 | 356 | 60 | 4.76e-04 | 3.39e-13 | 0 |
| etapa-B1 vs etapa-B2-teste | 356 | 62 | 4.52e-04 | 1.75e-13 | 0 |
| etapa-B1 vs etapa-B2 | 356 | 51 | 4.81e-04 | 2.10e-13 | 0 |
| etapa-B2-teste vs etapa-B2 | 356 | 20 | 4.72e-04 | 3.05e-13 | 0 |
