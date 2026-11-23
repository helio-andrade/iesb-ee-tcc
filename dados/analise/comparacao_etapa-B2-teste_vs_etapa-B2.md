# etapa-B2 em relação a etapa-B2-teste (teste t de Welch, IC 95%, p ajustado por Holm)

| caminho | teste | tamanho (B) | métrica | média A | média B | diferença | dif. % | IC 95% da diferença | p (Holm) | significativa |
|---|---|---|---|---|---|---|---|---|---|---|
| LAN-matriz | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| LAN-matriz | latencia | — | rtt_medio_ms | 6.68 | 5.06 | -1.62 | -24.3% | [-2.33; -0.912] | 0.00912 | sim |
| LAN-matriz | latencia | — | rtt_p95_ms | 8.62 | 7.54 | -1.08 | -12.5% | [-1.87; -0.292] | 1 | não |
| LAN-matriz | tcp | — | retrans | 1.54e+03 | 1.5e+03 | -42.1 | -2.7% | [-86.6; 2.36] | 1 | não |
| LAN-matriz | tcp | — | vazao_mbps | 80.6 | 78.9 | -1.67 | -2.1% | [-4.35; 1] | 1 | não |
| LAN-matriz | udp | 1024 | jitter_ms | 0.0663 | 0.0538 | -0.0125 | -18.8% | [-0.0523; 0.0274] | 1 | não |
| LAN-matriz | udp | 1024 | perda_pct | 19.3 | 20.7 | +1.44 | +7.4% | [-0.286; 3.16] | 1 | não |
| LAN-matriz | udp | 1024 | vazao_mbps | 72.6 | 71.3 | -1.29 | -1.8% | [-2.84; 0.257] | 1 | não |
| LAN-matriz | udp | 1400 | jitter_ms | 0.0502 | 0.0533 | +0.00303 | +6.0% | [-0.0171; 0.0232] | 1 | não |
| LAN-matriz | udp | 1400 | perda_pct | 5.34 | 5.77 | +0.431 | +8.1% | [-0.674; 1.54] | 1 | não |
| LAN-matriz | udp | 1400 | vazao_mbps | 85.2 | 84.8 | -0.389 | -0.5% | [-1.38; 0.606] | 1 | não |
| LAN-matriz | udp | 512 | jitter_ms | 0.0856 | 0.0914 | +0.00583 | +6.8% | [-0.0234; 0.035] | 1 | não |
| LAN-matriz | udp | 512 | perda_pct | 46.5 | 47.4 | +0.929 | +2.0% | [-0.156; 2.01] | 1 | não |
| LAN-matriz | udp | 512 | vazao_mbps | 48.1 | 47.3 | -0.835 | -1.7% | [-1.81; 0.142] | 1 | não |
| LAN-matriz | udp | 64 | jitter_ms | 0.371 | 0.245 | -0.126 | -34.0% | [-0.32; 0.0678] | 1 | não |
| LAN-matriz | udp | 64 | perda_pct | 96 | 95.2 | -0.769 | -0.8% | [-1.44; -0.0969] | 1 | não |
| LAN-matriz | udp | 64 | vazao_mbps | 3.62 | 4.31 | +0.692 | +19.1% | [0.087; 1.3] | 1 | não |
| filial1-filial2 | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| filial1-filial2 | latencia | — | rtt_medio_ms | 94.1 | 89.3 | -4.77 | -5.1% | [-6.14; -3.4] | 1.12e-06 | sim |
| filial1-filial2 | latencia | — | rtt_p95_ms | 96.7 | 91.3 | -5.46 | -5.6% | [-6.77; -4.15] | 5.71e-09 | sim |
| filial1-filial2 | tcp | — | retrans | 4.67 | 8.07 | +3.4 | +72.9% | [-7.11; 13.9] | 1 | não |
| filial1-filial2 | tcp | — | vazao_mbps | 8.92 | 8.91 | -0.0103 | -0.1% | [-0.028; 0.00743] | 1 | não |
| filial1-filial2 | udp | 1024 | jitter_ms | 0.437 | 0.355 | -0.082 | -18.8% | [-0.201; 0.0372] | 1 | não |
| filial1-filial2 | udp | 1024 | perda_pct | 0.0873 | 0.0903 | +0.00297 | +3.4% | [-0.142; 0.148] | 1 | não |
| filial1-filial2 | udp | 1024 | vazao_mbps | 8.99 | 8.99 | -0.0002 | -0.0% | [-0.0132; 0.0128] | 1 | não |
| filial1-filial2 | udp | 1400 | jitter_ms | 0.411 | 0.501 | +0.09 | +21.9% | [0.00194; 0.178] | 1 | não |
| filial1-filial2 | udp | 1400 | perda_pct | 0.12 | 0.142 | +0.0228 | +19.1% | [-0.221; 0.266] | 1 | não |
| filial1-filial2 | udp | 1400 | vazao_mbps | 8.99 | 8.99 | -0.002 | -0.0% | [-0.0239; 0.0199] | 1 | não |
| filial1-filial2 | udp | 512 | jitter_ms | 0.51 | 0.528 | +0.0179 | +3.5% | [-0.0419; 0.0777] | 1 | não |
| filial1-filial2 | udp | 512 | perda_pct | 0.193 | 0.339 | +0.145 | +75.3% | [-0.143; 0.434] | 1 | não |
| filial1-filial2 | udp | 512 | vazao_mbps | 8.98 | 8.97 | -0.013 | -0.1% | [-0.0391; 0.013] | 1 | não |
| filial1-filial2 | udp | 64 | jitter_ms | 0.179 | 0.179 | -0.000782 | -0.4% | [-0.0293; 0.0277] | 1 | não |
| filial1-filial2 | udp | 64 | perda_pct | 60.8 | 62.2 | +1.35 | +2.2% | [-1.32; 4.02] | 1 | não |
| filial1-filial2 | udp | 64 | vazao_mbps | 3.52 | 3.4 | -0.122 | -3.5% | [-0.362; 0.119] | 1 | não |
| matriz-filial1 | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| matriz-filial1 | latencia | — | rtt_medio_ms | 29.9 | 27.8 | -2.09 | -7.0% | [-3.33; -0.843] | 0.457 | não |
| matriz-filial1 | latencia | — | rtt_p95_ms | 32.6 | 30.2 | -2.38 | -7.3% | [-3.74; -1.02] | 0.302 | não |
| matriz-filial1 | tcp | — | retrans | 1.9 | 7.57 | +5.67 | +298.2% | [-9.15; 20.5] | 1 | não |
| matriz-filial1 | tcp | — | vazao_mbps | 18.2 | 18.2 | -0.00377 | -0.0% | [-0.0106; 0.00307] | 1 | não |
| matriz-filial1 | udp | 1024 | jitter_ms | 0.362 | 0.465 | +0.103 | +28.4% | [-0.00343; 0.209] | 1 | não |
| matriz-filial1 | udp | 1024 | perda_pct | 0.802 | 0.907 | +0.105 | +13.1% | [-0.841; 1.05] | 1 | não |
| matriz-filial1 | udp | 1024 | vazao_mbps | 17.9 | 17.8 | -0.0195 | -0.1% | [-0.19; 0.151] | 1 | não |
| matriz-filial1 | udp | 1400 | jitter_ms | 0.372 | 0.343 | -0.03 | -8.0% | [-0.195; 0.135] | 1 | não |
| matriz-filial1 | udp | 1400 | perda_pct | 0.105 | 0.308 | +0.204 | +194.1% | [-0.0761; 0.483] | 1 | não |
| matriz-filial1 | udp | 1400 | vazao_mbps | 18 | 17.9 | -0.0364 | -0.2% | [-0.0867; 0.014] | 1 | não |
| matriz-filial1 | udp | 512 | jitter_ms | 0.347 | 0.346 | -0.00117 | -0.3% | [-0.0248; 0.0225] | 1 | não |
| matriz-filial1 | udp | 512 | perda_pct | 6.55 | 8.95 | +2.4 | +36.6% | [1.23; 3.57] | 0.0435 | sim |
| matriz-filial1 | udp | 512 | vazao_mbps | 16.8 | 16.4 | -0.431 | -2.6% | [-0.642; -0.221] | 0.0435 | sim |
| matriz-filial1 | udp | 64 | jitter_ms | 0.0948 | 0.109 | +0.0139 | +14.6% | [-0.0197; 0.0475] | 1 | não |
| matriz-filial1 | udp | 64 | perda_pct | 68.3 | 69.4 | +1.06 | +1.5% | [-0.153; 2.27] | 1 | não |
| matriz-filial1 | udp | 64 | vazao_mbps | 5.7 | 5.51 | -0.191 | -3.3% | [-0.409; 0.0275] | 1 | não |
| matriz-filial2 | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| matriz-filial2 | latencia | — | rtt_medio_ms | 70.7 | 67.5 | -3.15 | -4.5% | [-4.15; -2.15] | 1.6e-05 | sim |
| matriz-filial2 | latencia | — | rtt_p95_ms | 73.2 | 70.2 | -2.99 | -4.1% | [-4.14; -1.84] | 0.000963 | sim |
| matriz-filial2 | tcp | — | retrans | 3.8 | 0.5 | -3.3 | -86.8% | [-6.75; 0.152] | 1 | não |
| matriz-filial2 | tcp | — | vazao_mbps | 8.77 | 9.02 | +0.245 | +2.8% | [-0.0732; 0.562] | 1 | não |
| matriz-filial2 | udp | 1024 | jitter_ms | 0.294 | 0.297 | +0.00263 | +0.9% | [-0.0678; 0.0731] | 1 | não |
| matriz-filial2 | udp | 1024 | perda_pct | 0.0874 | 0.0732 | -0.0142 | -16.2% | [-0.152; 0.124] | 1 | não |
| matriz-filial2 | udp | 1024 | vazao_mbps | 8.99 | 8.99 | +0.0012 | +0.0% | [-0.0112; 0.0136] | 1 | não |
| matriz-filial2 | udp | 1400 | jitter_ms | 0.245 | 0.296 | +0.0512 | +20.9% | [0.00565; 0.0967] | 1 | não |
| matriz-filial2 | udp | 1400 | perda_pct | 0.137 | 0 | -0.137 | -100.0% | [-0.275; 0.00228] | 1 | não |
| matriz-filial2 | udp | 1400 | vazao_mbps | 8.99 | 9 | +0.0123 | +0.1% | [-0.000324; 0.0249] | 1 | não |
| matriz-filial2 | udp | 512 | jitter_ms | 0.504 | 0.497 | -0.00773 | -1.5% | [-0.04; 0.0245] | 1 | não |
| matriz-filial2 | udp | 512 | perda_pct | 0.168 | 0.333 | +0.165 | +98.6% | [-0.355; 0.686] | 1 | não |
| matriz-filial2 | udp | 512 | vazao_mbps | 8.98 | 8.97 | -0.0147 | -0.2% | [-0.0615; 0.0321] | 1 | não |
| matriz-filial2 | udp | 64 | jitter_ms | 0.235 | 0.207 | -0.0278 | -11.8% | [-0.08; 0.0244] | 1 | não |
| matriz-filial2 | udp | 64 | perda_pct | 65.1 | 63.9 | -1.17 | -1.8% | [-3.63; 1.29] | 1 | não |
| matriz-filial2 | udp | 64 | vazao_mbps | 3.14 | 3.24 | +0.105 | +3.3% | [-0.116; 0.327] | 1 | não |