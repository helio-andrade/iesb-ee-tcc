# etapa-B2 em relação a etapa-B1 (teste t de Welch, IC 95%, p ajustado por Holm)

| caminho | teste | tamanho (B) | métrica | média A | média B | diferença | dif. % | IC 95% da diferença | p (Holm) | significativa |
|---|---|---|---|---|---|---|---|---|---|---|
| LAN-matriz | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| LAN-matriz | latencia | — | rtt_medio_ms | 5.15 | 5.06 | -0.0925 | -1.8% | [-0.845; 0.66] | 1 | não |
| LAN-matriz | latencia | — | rtt_p95_ms | 7.39 | 7.54 | +0.148 | +2.0% | [-0.756; 1.05] | 1 | não |
| LAN-matriz | tcp | — | retrans | 1.5e+03 | 1.5e+03 | +2.73 | +0.2% | [-36; 41.4] | 1 | não |
| LAN-matriz | tcp | — | vazao_mbps | 79 | 78.9 | -0.0957 | -0.1% | [-1.83; 1.64] | 1 | não |
| LAN-matriz | udp | 1024 | jitter_ms | 0.0652 | 0.0538 | -0.0114 | -17.5% | [-0.0402; 0.0174] | 1 | não |
| LAN-matriz | udp | 1024 | perda_pct | 20.1 | 20.7 | +0.58 | +2.9% | [-1.54; 2.7] | 1 | não |
| LAN-matriz | udp | 1024 | vazao_mbps | 71.9 | 71.3 | -0.522 | -0.7% | [-2.43; 1.38] | 1 | não |
| LAN-matriz | udp | 1400 | jitter_ms | 0.0596 | 0.0533 | -0.0063 | -10.6% | [-0.0296; 0.017] | 1 | não |
| LAN-matriz | udp | 1400 | perda_pct | 6.38 | 5.77 | -0.611 | -9.6% | [-2.31; 1.09] | 1 | não |
| LAN-matriz | udp | 1400 | vazao_mbps | 84.2 | 84.8 | +0.548 | +0.7% | [-0.981; 2.08] | 1 | não |
| LAN-matriz | udp | 512 | jitter_ms | 0.0917 | 0.0914 | -0.000267 | -0.3% | [-0.0323; 0.0318] | 1 | não |
| LAN-matriz | udp | 512 | perda_pct | 48.5 | 47.4 | -1.03 | -2.1% | [-2.3; 0.234] | 1 | não |
| LAN-matriz | udp | 512 | vazao_mbps | 46.4 | 47.3 | +0.928 | +2.0% | [-0.21; 2.07] | 1 | não |
| LAN-matriz | udp | 64 | jitter_ms | 0.182 | 0.245 | +0.0632 | +34.7% | [-0.0997; 0.226] | 1 | não |
| LAN-matriz | udp | 64 | perda_pct | 95.5 | 95.2 | -0.275 | -0.3% | [-0.897; 0.346] | 1 | não |
| LAN-matriz | udp | 64 | vazao_mbps | 4.07 | 4.31 | +0.248 | +6.1% | [-0.312; 0.807] | 1 | não |
| filial1-filial2 | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| filial1-filial2 | latencia | — | rtt_medio_ms | 88.3 | 89.3 | +1.01 | +1.1% | [-0.2; 2.23] | 1 | não |
| filial1-filial2 | latencia | — | rtt_p95_ms | 90.7 | 91.3 | +0.527 | +0.6% | [-0.76; 1.81] | 1 | não |
| filial1-filial2 | tcp | — | retrans | 2.97 | 8.07 | +5.1 | +171.9% | [-4.8; 15] | 1 | não |
| filial1-filial2 | tcp | — | vazao_mbps | 9.3 | 8.91 | -0.39 | -4.2% | [-0.413; -0.368] | 1.85e-37 | sim |
| filial1-filial2 | udp | 1024 | jitter_ms | 0.362 | 0.355 | -0.00723 | -2.0% | [-0.0503; 0.0359] | 1 | não |
| filial1-filial2 | udp | 1024 | perda_pct | 0.114 | 0.0903 | -0.0236 | -20.7% | [-0.189; 0.142] | 1 | não |
| filial1-filial2 | udp | 1024 | vazao_mbps | 8.99 | 8.99 | +0.00233 | +0.0% | [-0.0125; 0.0171] | 1 | não |
| filial1-filial2 | udp | 1400 | jitter_ms | 0.415 | 0.501 | +0.0865 | +20.9% | [-0.00275; 0.176] | 1 | não |
| filial1-filial2 | udp | 1400 | perda_pct | 0.0114 | 0.142 | +0.131 | +1148.2% | [-0.0646; 0.326] | 1 | não |
| filial1-filial2 | udp | 1400 | vazao_mbps | 9 | 8.99 | -0.0116 | -0.1% | [-0.0292; 0.00599] | 1 | não |
| filial1-filial2 | udp | 512 | jitter_ms | 0.219 | 0.528 | +0.308 | +140.8% | [0.247; 0.37] | 1.57e-10 | sim |
| filial1-filial2 | udp | 512 | perda_pct | 0.206 | 0.339 | +0.132 | +63.9% | [-0.166; 0.43] | 1 | não |
| filial1-filial2 | udp | 512 | vazao_mbps | 8.98 | 8.97 | -0.012 | -0.1% | [-0.0388; 0.0149] | 1 | não |
| filial1-filial2 | udp | 64 | jitter_ms | 0.112 | 0.179 | +0.0667 | +59.6% | [0.0406; 0.0927] | 0.00121 | sim |
| filial1-filial2 | udp | 64 | perda_pct | 42.6 | 62.2 | +19.5 | +45.8% | [16.9; 22.2] | 1.19e-12 | sim |
| filial1-filial2 | udp | 64 | vazao_mbps | 5.16 | 3.4 | -1.76 | -34.1% | [-2; -1.52] | 1.19e-12 | sim |
| matriz-filial1 | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| matriz-filial1 | latencia | — | rtt_medio_ms | 27.5 | 27.8 | +0.339 | +1.2% | [-0.903; 1.58] | 1 | não |
| matriz-filial1 | latencia | — | rtt_p95_ms | 30.2 | 30.2 | +0.0467 | +0.2% | [-1.39; 1.49] | 1 | não |
| matriz-filial1 | tcp | — | retrans | 13.1 | 7.57 | -5.57 | -42.4% | [-25.4; 14.3] | 1 | não |
| matriz-filial1 | tcp | — | vazao_mbps | 19 | 18.2 | -0.781 | -4.1% | [-0.793; -0.768] | 9.02e-55 | sim |
| matriz-filial1 | udp | 1024 | jitter_ms | 0.272 | 0.465 | +0.193 | +70.9% | [0.0907; 0.295] | 0.155 | não |
| matriz-filial1 | udp | 1024 | perda_pct | 0.13 | 0.907 | +0.777 | +599.6% | [0.00877; 1.55] | 1 | não |
| matriz-filial1 | udp | 1024 | vazao_mbps | 18 | 17.8 | -0.14 | -0.8% | [-0.279; -0.00218] | 1 | não |
| matriz-filial1 | udp | 1400 | jitter_ms | 0.302 | 0.343 | +0.04 | +13.2% | [-0.0677; 0.148] | 1 | não |
| matriz-filial1 | udp | 1400 | perda_pct | 0.257 | 0.308 | +0.0516 | +20.1% | [-0.28; 0.383] | 1 | não |
| matriz-filial1 | udp | 1400 | vazao_mbps | 18 | 17.9 | -0.00917 | -0.1% | [-0.0688; 0.0504] | 1 | não |
| matriz-filial1 | udp | 512 | jitter_ms | 0.343 | 0.346 | +0.00353 | +1.0% | [-0.0197; 0.0268] | 1 | não |
| matriz-filial1 | udp | 512 | perda_pct | 7.94 | 8.95 | +1 | +12.7% | [-0.191; 2.2] | 1 | não |
| matriz-filial1 | udp | 512 | vazao_mbps | 16.6 | 16.4 | -0.181 | -1.1% | [-0.396; 0.0343] | 1 | não |
| matriz-filial1 | udp | 64 | jitter_ms | 0.12 | 0.109 | -0.0112 | -9.4% | [-0.0621; 0.0396] | 1 | não |
| matriz-filial1 | udp | 64 | perda_pct | 65.3 | 69.4 | +4.14 | +6.3% | [2.96; 5.32] | 2.06e-06 | sim |
| matriz-filial1 | udp | 64 | vazao_mbps | 6.25 | 5.51 | -0.745 | -11.9% | [-0.957; -0.532] | 2.05e-06 | sim |
| matriz-filial2 | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| matriz-filial2 | latencia | — | rtt_medio_ms | 68 | 67.5 | -0.444 | -0.7% | [-1.4; 0.512] | 1 | não |
| matriz-filial2 | latencia | — | rtt_p95_ms | 70.9 | 70.2 | -0.677 | -1.0% | [-1.83; 0.479] | 1 | não |
| matriz-filial2 | tcp | — | retrans | 0.7 | 0.5 | -0.2 | -28.6% | [-1.1; 0.702] | 1 | não |
| matriz-filial2 | tcp | — | vazao_mbps | 9.33 | 9.02 | -0.309 | -3.3% | [-0.318; -0.3] | 2.83e-52 | sim |
| matriz-filial2 | udp | 1024 | jitter_ms | 0.246 | 0.297 | +0.0511 | +20.8% | [-0.00335; 0.106] | 1 | não |
| matriz-filial2 | udp | 1024 | perda_pct | 0.00413 | 0.0732 | +0.0691 | +1671.0% | [-0.0299; 0.168] | 1 | não |
| matriz-filial2 | udp | 1024 | vazao_mbps | 9 | 8.99 | -0.00653 | -0.1% | [-0.0154; 0.00235] | 1 | não |
| matriz-filial2 | udp | 1400 | jitter_ms | 0.28 | 0.296 | +0.0156 | +5.6% | [-0.0417; 0.0728] | 1 | não |
| matriz-filial2 | udp | 1400 | perda_pct | 0.0382 | 0 | -0.0382 | -100.0% | [-0.111; 0.0349] | 1 | não |
| matriz-filial2 | udp | 1400 | vazao_mbps | 9 | 9 | +0.00333 | +0.0% | [-0.00327; 0.00993] | 1 | não |
| matriz-filial2 | udp | 512 | jitter_ms | 0.171 | 0.497 | +0.326 | +190.9% | [0.287; 0.365] | 8.15e-21 | sim |
| matriz-filial2 | udp | 512 | perda_pct | 0.22 | 0.333 | +0.114 | +51.8% | [-0.407; 0.634] | 1 | não |
| matriz-filial2 | udp | 512 | vazao_mbps | 8.98 | 8.97 | -0.0101 | -0.1% | [-0.0568; 0.0367] | 1 | não |
| matriz-filial2 | udp | 64 | jitter_ms | 0.139 | 0.207 | +0.0682 | +49.0% | [0.0285; 0.108] | 0.325 | não |
| matriz-filial2 | udp | 64 | perda_pct | 42.7 | 63.9 | +21.3 | +49.8% | [21.2; 21.3] | 1.59e-114 | sim |
| matriz-filial2 | udp | 64 | vazao_mbps | 5.16 | 3.24 | -1.91 | -37.1% | [-1.92; -1.91] | 7.94e-115 | sim |