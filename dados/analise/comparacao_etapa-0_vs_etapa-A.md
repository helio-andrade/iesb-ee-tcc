# etapa-A em relação a etapa-0 (teste t de Welch, IC 95%, p ajustado por Holm)

| caminho | teste | tamanho (B) | métrica | média A | média B | diferença | dif. % | IC 95% da diferença | p (Holm) | significativa |
|---|---|---|---|---|---|---|---|---|---|---|
| LAN-matriz | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| LAN-matriz | latencia | — | rtt_medio_ms | 3.64 | 3.97 | +0.33 | +9.1% | [0.00598; 0.655] | 1 | não |
| LAN-matriz | latencia | — | rtt_p95_ms | 4.75 | 5.16 | +0.415 | +8.8% | [0.18; 0.651] | 0.237 | não |
| LAN-matriz | tcp | — | retrans | 2.95e+03 | 2.8e+03 | -151 | -5.1% | [-232; -70.8] | 0.115 | não |
| LAN-matriz | tcp | — | vazao_mbps | 160 | 143 | -17.9 | -11.2% | [-21.2; -14.6] | 5.89e-11 | sim |
| LAN-matriz | udp | 1024 | jitter_ms | 0.0235 | 0.0411 | +0.0176 | +74.9% | [0.00439; 0.0308] | 1 | não |
| LAN-matriz | udp | 1024 | perda_pct | 18.7 | 20.8 | +2.03 | +10.9% | [-5.84; 9.91] | 1 | não |
| LAN-matriz | udp | 1024 | vazao_mbps | 73.1 | 71.3 | -1.83 | -2.5% | [-8.92; 5.26] | 1 | não |
| LAN-matriz | udp | 1400 | jitter_ms | 0.0551 | 0.0499 | -0.00517 | -9.4% | [-0.0388; 0.0284] | 1 | não |
| LAN-matriz | udp | 1400 | perda_pct | 6.38 | 7.31 | +0.927 | +14.5% | [-8.19; 10] | 1 | não |
| LAN-matriz | udp | 1400 | vazao_mbps | 84.2 | 83.4 | -0.833 | -1.0% | [-9.03; 7.37] | 1 | não |
| LAN-matriz | udp | 512 | jitter_ms | 0.0181 | 0.0319 | +0.0137 | +75.7% | [0.00751; 0.0199] | 0.02 | sim |
| LAN-matriz | udp | 512 | perda_pct | 28.3 | 32.1 | +3.77 | +13.3% | [-1.4; 8.94] | 1 | não |
| LAN-matriz | udp | 512 | vazao_mbps | 62.1 | 61.1 | -0.991 | -1.6% | [-6.23; 4.25] | 1 | não |
| LAN-matriz | udp | 64 | jitter_ms | 0.0126 | 0.0245 | +0.012 | +95.2% | [0.0035; 0.0204] | 1 | não |
| LAN-matriz | udp | 64 | perda_pct | 85.8 | 85.7 | -0.0434 | -0.1% | [-6.1; 6.01] | 1 | não |
| LAN-matriz | udp | 64 | vazao_mbps | 12.8 | 10.4 | -2.36 | -18.5% | [-2.97; -1.75] | 5.27e-07 | sim |
| filial1-filial2 | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| filial1-filial2 | latencia | — | rtt_medio_ms | 89.6 | 89.4 | -0.22 | -0.2% | [-1.07; 0.63] | 1 | não |
| filial1-filial2 | latencia | — | rtt_p95_ms | 91.7 | 91.8 | +0.163 | +0.2% | [-0.599; 0.926] | 1 | não |
| filial1-filial2 | tcp | — | retrans | 1.27 | 3.07 | +1.8 | +142.1% | [-2.89; 6.49] | 1 | não |
| filial1-filial2 | tcp | — | vazao_mbps | 9.29 | 9.06 | -0.232 | -2.5% | [-0.549; 0.0855] | 1 | não |
| filial1-filial2 | udp | 1024 | jitter_ms | 0.323 | 0.312 | -0.0114 | -3.5% | [-0.0377; 0.015] | 1 | não |
| filial1-filial2 | udp | 1024 | perda_pct | 0.0342 | 0.0597 | +0.0254 | +74.3% | [-0.0484; 0.0993] | 1 | não |
| filial1-filial2 | udp | 1024 | vazao_mbps | 9 | 8.99 | -0.00213 | -0.0% | [-0.00886; 0.00459] | 1 | não |
| filial1-filial2 | udp | 1400 | jitter_ms | 0.396 | 0.387 | -0.00943 | -2.4% | [-0.0498; 0.0309] | 1 | não |
| filial1-filial2 | udp | 1400 | perda_pct | 0.00243 | 0.0732 | +0.0707 | +2906.8% | [-0.0508; 0.192] | 1 | não |
| filial1-filial2 | udp | 1400 | vazao_mbps | 9 | 8.99 | -0.00633 | -0.1% | [-0.0172; 0.00457] | 1 | não |
| filial1-filial2 | udp | 512 | jitter_ms | 0.241 | 0.212 | -0.0285 | -11.8% | [-0.0721; 0.0152] | 1 | não |
| filial1-filial2 | udp | 512 | perda_pct | 0.169 | 0.049 | -0.12 | -71.0% | [-0.274; 0.0343] | 1 | não |
| filial1-filial2 | udp | 512 | vazao_mbps | 8.98 | 8.99 | +0.0106 | +0.1% | [-0.0032; 0.0245] | 1 | não |
| filial1-filial2 | udp | 64 | jitter_ms | 0.0916 | 0.0871 | -0.00453 | -4.9% | [-0.0118; 0.00274] | 1 | não |
| filial1-filial2 | udp | 64 | perda_pct | 42.9 | 42.7 | -0.236 | -0.6% | [-0.632; 0.16] | 1 | não |
| filial1-filial2 | udp | 64 | vazao_mbps | 5.14 | 5.16 | +0.0212 | +0.4% | [-0.0144; 0.0568] | 1 | não |
| matriz-filial1 | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| matriz-filial1 | latencia | — | rtt_medio_ms | 29.5 | 29.5 | -0.0243 | -0.1% | [-1.03; 0.981] | 1 | não |
| matriz-filial1 | latencia | — | rtt_p95_ms | 32.5 | 32.2 | -0.277 | -0.9% | [-1.25; 0.694] | 1 | não |
| matriz-filial1 | tcp | — | retrans | 5.17 | 0.733 | -4.43 | -85.8% | [-13.1; 4.22] | 1 | não |
| matriz-filial1 | tcp | — | vazao_mbps | 19 | 19 | -0.0211 | -0.1% | [-0.0631; 0.0208] | 1 | não |
| matriz-filial1 | udp | 1024 | jitter_ms | 0.272 | 0.324 | +0.0519 | +19.1% | [-0.0563; 0.16] | 1 | não |
| matriz-filial1 | udp | 1024 | perda_pct | 0.029 | 0.191 | +0.162 | +560.2% | [-0.0241; 0.349] | 1 | não |
| matriz-filial1 | udp | 1024 | vazao_mbps | 18 | 18 | -0.0289 | -0.2% | [-0.0625; 0.00465] | 1 | não |
| matriz-filial1 | udp | 1400 | jitter_ms | 0.335 | 0.267 | -0.0678 | -20.2% | [-0.146; 0.0107] | 1 | não |
| matriz-filial1 | udp | 1400 | perda_pct | 0.0191 | 0.1 | +0.0813 | +425.8% | [0.00969; 0.153] | 1 | não |
| matriz-filial1 | udp | 1400 | vazao_mbps | 18 | 18 | -0.0149 | -0.1% | [-0.0278; -0.00196] | 1 | não |
| matriz-filial1 | udp | 512 | jitter_ms | 0.312 | 0.326 | +0.0144 | +4.6% | [-0.0291; 0.0579] | 1 | não |
| matriz-filial1 | udp | 512 | perda_pct | 2.95 | 4.95 | +2 | +67.9% | [1.25; 2.76] | 0.000675 | sim |
| matriz-filial1 | udp | 512 | vazao_mbps | 17.5 | 17.1 | -0.361 | -2.1% | [-0.497; -0.225] | 0.00067 | sim |
| matriz-filial1 | udp | 64 | jitter_ms | 0.0992 | 0.0456 | -0.0536 | -54.0% | [-0.125; 0.0176] | 1 | não |
| matriz-filial1 | udp | 64 | perda_pct | 64.1 | 67.7 | +3.6 | +5.6% | [1.97; 5.24] | 0.0147 | sim |
| matriz-filial1 | udp | 64 | vazao_mbps | 6.46 | 5.81 | -0.649 | -10.1% | [-0.944; -0.354] | 0.0146 | sim |
| matriz-filial2 | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| matriz-filial2 | latencia | — | rtt_medio_ms | 69.3 | 69.8 | +0.546 | +0.8% | [-0.535; 1.63] | 1 | não |
| matriz-filial2 | latencia | — | rtt_p95_ms | 71.9 | 72.2 | +0.263 | +0.4% | [-0.659; 1.19] | 1 | não |
| matriz-filial2 | tcp | — | retrans | 1.83 | 2.33 | +0.5 | +27.3% | [-3.71; 4.71] | 1 | não |
| matriz-filial2 | tcp | — | vazao_mbps | 9.32 | 9.32 | -0.0014 | -0.0% | [-0.012; 0.00918] | 1 | não |
| matriz-filial2 | udp | 1024 | jitter_ms | 0.249 | 0.345 | +0.0967 | +38.9% | [-0.025; 0.218] | 1 | não |
| matriz-filial2 | udp | 1024 | perda_pct | 0.00473 | 0.0502 | +0.0454 | +959.9% | [2.86e-05; 0.0908] | 1 | não |
| matriz-filial2 | udp | 1024 | vazao_mbps | 9 | 8.99 | -0.00417 | -0.0% | [-0.00828; -5.13e-05] | 1 | não |
| matriz-filial2 | udp | 1400 | jitter_ms | 0.285 | 0.289 | +0.00357 | +1.2% | [-0.0515; 0.0586] | 1 | não |
| matriz-filial2 | udp | 1400 | perda_pct | 0.0374 | 0.0122 | -0.0252 | -67.4% | [-0.0707; 0.0203] | 1 | não |
| matriz-filial2 | udp | 1400 | vazao_mbps | 9 | 9 | +0.00233 | +0.0% | [-0.00173; 0.0064] | 1 | não |
| matriz-filial2 | udp | 512 | jitter_ms | 0.192 | 0.19 | -0.0019 | -1.0% | [-0.0782; 0.0744] | 1 | não |
| matriz-filial2 | udp | 512 | perda_pct | 0.127 | 0.122 | -0.00543 | -4.3% | [-0.183; 0.173] | 1 | não |
| matriz-filial2 | udp | 512 | vazao_mbps | 8.99 | 8.99 | +0.000733 | +0.0% | [-0.0153; 0.0167] | 1 | não |
| matriz-filial2 | udp | 64 | jitter_ms | 0.116 | 0.123 | +0.0069 | +5.9% | [-0.0297; 0.0435] | 1 | não |
| matriz-filial2 | udp | 64 | perda_pct | 42.7 | 42.8 | +0.121 | +0.3% | [-0.0188; 0.261] | 1 | não |
| matriz-filial2 | udp | 64 | vazao_mbps | 5.16 | 5.15 | -0.0109 | -0.2% | [-0.0235; 0.00165] | 1 | não |