# etapa-B2 em relação a etapa-0 (teste t de Welch, IC 95%, p ajustado por Holm)

| caminho | teste | tamanho (B) | métrica | média A | média B | diferença | dif. % | IC 95% da diferença | p (Holm) | significativa |
|---|---|---|---|---|---|---|---|---|---|---|
| LAN-matriz | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| LAN-matriz | latencia | — | rtt_medio_ms | 3.64 | 5.06 | +1.42 | +39.1% | [0.828; 2.01] | 0.00457 | sim |
| LAN-matriz | latencia | — | rtt_p95_ms | 4.75 | 7.54 | +2.8 | +58.9% | [2.08; 3.51] | 8.65e-07 | sim |
| LAN-matriz | tcp | — | retrans | 2.95e+03 | 1.5e+03 | -1.45e+03 | -49.1% | [-1.52e+03; -1.38e+03] | 7.54e-33 | sim |
| LAN-matriz | tcp | — | vazao_mbps | 160 | 78.9 | -81.5 | -50.8% | [-84.9; -78.2] | 1.8e-35 | sim |
| LAN-matriz | udp | 1024 | jitter_ms | 0.0235 | 0.0538 | +0.0303 | +128.9% | [0.012; 0.0487] | 0.352 | não |
| LAN-matriz | udp | 1024 | perda_pct | 18.7 | 20.7 | +1.99 | +10.6% | [-3.96; 7.94] | 1 | não |
| LAN-matriz | udp | 1024 | vazao_mbps | 73.1 | 71.3 | -1.79 | -2.4% | [-7.14; 3.56] | 1 | não |
| LAN-matriz | udp | 1400 | jitter_ms | 0.0551 | 0.0533 | -0.00184 | -3.3% | [-0.0339; 0.0303] | 1 | não |
| LAN-matriz | udp | 1400 | perda_pct | 6.38 | 5.77 | -0.608 | -9.5% | [-7.27; 6.05] | 1 | não |
| LAN-matriz | udp | 1400 | vazao_mbps | 84.2 | 84.8 | +0.546 | +0.6% | [-5.45; 6.54] | 1 | não |
| LAN-matriz | udp | 512 | jitter_ms | 0.0181 | 0.0914 | +0.0733 | +404.0% | [0.0518; 0.0948] | 2.62e-05 | sim |
| LAN-matriz | udp | 512 | perda_pct | 28.3 | 47.4 | +19.1 | +67.3% | [16.9; 21.3] | 1.84e-17 | sim |
| LAN-matriz | udp | 512 | vazao_mbps | 62.1 | 47.3 | -14.8 | -23.8% | [-18; -11.6] | 2.84e-08 | sim |
| LAN-matriz | udp | 64 | jitter_ms | 0.0126 | 0.245 | +0.233 | +1851.5% | [0.103; 0.363] | 0.203 | não |
| LAN-matriz | udp | 64 | perda_pct | 85.8 | 95.2 | +9.42 | +11.0% | [8.97; 9.87] | 2.64e-38 | sim |
| LAN-matriz | udp | 64 | vazao_mbps | 12.8 | 4.31 | -8.47 | -66.3% | [-8.88; -8.07] | 2.59e-38 | sim |
| filial1-filial2 | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| filial1-filial2 | latencia | — | rtt_medio_ms | 89.6 | 89.3 | -0.295 | -0.3% | [-1.46; 0.869] | 1 | não |
| filial1-filial2 | latencia | — | rtt_p95_ms | 91.7 | 91.3 | -0.393 | -0.4% | [-1.48; 0.698] | 1 | não |
| filial1-filial2 | tcp | — | retrans | 1.27 | 8.07 | +6.8 | +536.8% | [-2.79; 16.4] | 1 | não |
| filial1-filial2 | tcp | — | vazao_mbps | 9.29 | 8.91 | -0.389 | -4.2% | [-0.427; -0.351] | 3.32e-21 | sim |
| filial1-filial2 | udp | 1024 | jitter_ms | 0.323 | 0.355 | +0.0318 | +9.8% | [-0.00538; 0.0689] | 1 | não |
| filial1-filial2 | udp | 1024 | perda_pct | 0.0342 | 0.0903 | +0.0561 | +163.8% | [-0.0518; 0.164] | 1 | não |
| filial1-filial2 | udp | 1024 | vazao_mbps | 9 | 8.99 | -0.0048 | -0.1% | [-0.0145; 0.00491] | 1 | não |
| filial1-filial2 | udp | 1400 | jitter_ms | 0.396 | 0.501 | +0.105 | +26.5% | [0.0152; 0.194] | 1 | não |
| filial1-filial2 | udp | 1400 | perda_pct | 0.00243 | 0.142 | +0.14 | +5747.9% | [-0.0554; 0.335] | 1 | não |
| filial1-filial2 | udp | 1400 | vazao_mbps | 9 | 8.99 | -0.0123 | -0.1% | [-0.0299; 0.00523] | 1 | não |
| filial1-filial2 | udp | 512 | jitter_ms | 0.241 | 0.528 | +0.287 | +119.0% | [0.222; 0.352] | 2.16e-09 | sim |
| filial1-filial2 | udp | 512 | perda_pct | 0.169 | 0.339 | +0.17 | +100.4% | [-0.119; 0.458] | 1 | não |
| filial1-filial2 | udp | 512 | vazao_mbps | 8.98 | 8.97 | -0.0154 | -0.2% | [-0.0414; 0.0106] | 1 | não |
| filial1-filial2 | udp | 64 | jitter_ms | 0.0916 | 0.179 | +0.087 | +94.9% | [0.0695; 0.104] | 3.38e-09 | sim |
| filial1-filial2 | udp | 64 | perda_pct | 42.9 | 62.2 | +19.3 | +45.0% | [16.6; 22] | 8.64e-13 | sim |
| filial1-filial2 | udp | 64 | vazao_mbps | 5.14 | 3.4 | -1.74 | -33.8% | [-1.98; -1.49] | 8.64e-13 | sim |
| matriz-filial1 | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| matriz-filial1 | latencia | — | rtt_medio_ms | 29.5 | 27.8 | -1.7 | -5.8% | [-2.89; -0.523] | 0.974 | não |
| matriz-filial1 | latencia | — | rtt_p95_ms | 32.5 | 30.2 | -2.24 | -6.9% | [-3.39; -1.09] | 0.0663 | não |
| matriz-filial1 | tcp | — | retrans | 5.17 | 7.57 | +2.4 | +46.5% | [-14.4; 19.2] | 1 | não |
| matriz-filial1 | tcp | — | vazao_mbps | 19 | 18.2 | -0.787 | -4.1% | [-0.798; -0.775] | 1.7e-59 | sim |
| matriz-filial1 | udp | 1024 | jitter_ms | 0.272 | 0.465 | +0.194 | +71.2% | [0.0926; 0.294] | 0.0937 | não |
| matriz-filial1 | udp | 1024 | perda_pct | 0.029 | 0.907 | +0.878 | +3030.3% | [0.111; 1.64] | 1 | não |
| matriz-filial1 | udp | 1024 | vazao_mbps | 18 | 17.8 | -0.159 | -0.9% | [-0.296; -0.0206] | 1 | não |
| matriz-filial1 | udp | 1400 | jitter_ms | 0.335 | 0.343 | +0.0078 | +2.3% | [-0.0845; 0.1] | 1 | não |
| matriz-filial1 | udp | 1400 | perda_pct | 0.0191 | 0.308 | +0.289 | +1515.2% | [0.0277; 0.551] | 1 | não |
| matriz-filial1 | udp | 1400 | vazao_mbps | 18 | 17.9 | -0.0521 | -0.3% | [-0.0992; -0.005] | 1 | não |
| matriz-filial1 | udp | 512 | jitter_ms | 0.312 | 0.346 | +0.0346 | +11.1% | [-0.00515; 0.0743] | 1 | não |
| matriz-filial1 | udp | 512 | perda_pct | 2.95 | 8.95 | +5.99 | +203.2% | [5.03; 6.96] | 1.48e-13 | sim |
| matriz-filial1 | udp | 512 | vazao_mbps | 17.5 | 16.4 | -1.08 | -6.2% | [-1.25; -0.906] | 1.45e-13 | sim |
| matriz-filial1 | udp | 64 | jitter_ms | 0.0992 | 0.109 | +0.00947 | +9.5% | [-0.0647; 0.0836] | 1 | não |
| matriz-filial1 | udp | 64 | perda_pct | 64.1 | 69.4 | +5.28 | +8.2% | [3.7; 6.86] | 3.08e-06 | sim |
| matriz-filial1 | udp | 64 | vazao_mbps | 6.46 | 5.51 | -0.951 | -14.7% | [-1.24; -0.666] | 3.08e-06 | sim |
| matriz-filial2 | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| matriz-filial2 | latencia | — | rtt_medio_ms | 69.3 | 67.5 | -1.73 | -2.5% | [-2.74; -0.721] | 0.225 | não |
| matriz-filial2 | latencia | — | rtt_p95_ms | 71.9 | 70.2 | -1.71 | -2.4% | [-2.71; -0.704] | 0.251 | não |
| matriz-filial2 | tcp | — | retrans | 1.83 | 0.5 | -1.33 | -72.7% | [-3.46; 0.79] | 1 | não |
| matriz-filial2 | tcp | — | vazao_mbps | 9.32 | 9.02 | -0.305 | -3.3% | [-0.315; -0.295] | 3.01e-45 | sim |
| matriz-filial2 | udp | 1024 | jitter_ms | 0.249 | 0.297 | +0.0483 | +19.4% | [-0.00114; 0.0977] | 1 | não |
| matriz-filial2 | udp | 1024 | perda_pct | 0.00473 | 0.0732 | +0.0685 | +1446.5% | [-0.0307; 0.168] | 1 | não |
| matriz-filial2 | udp | 1024 | vazao_mbps | 9 | 8.99 | -0.00617 | -0.1% | [-0.0151; 0.00274] | 1 | não |
| matriz-filial2 | udp | 1400 | jitter_ms | 0.285 | 0.296 | +0.0103 | +3.6% | [-0.0481; 0.0687] | 1 | não |
| matriz-filial2 | udp | 1400 | perda_pct | 0.0374 | 0 | -0.0374 | -100.0% | [-0.081; 0.0063] | 1 | não |
| matriz-filial2 | udp | 1400 | vazao_mbps | 9 | 9 | +0.00343 | +0.0% | [-0.000477; 0.00734] | 1 | não |
| matriz-filial2 | udp | 512 | jitter_ms | 0.192 | 0.497 | +0.305 | +159.1% | [0.242; 0.368] | 1.62e-09 | sim |
| matriz-filial2 | udp | 512 | perda_pct | 0.127 | 0.333 | +0.206 | +162.3% | [-0.307; 0.719] | 1 | não |
| matriz-filial2 | udp | 512 | vazao_mbps | 8.99 | 8.97 | -0.0184 | -0.2% | [-0.0645; 0.0277] | 1 | não |
| matriz-filial2 | udp | 64 | jitter_ms | 0.116 | 0.207 | +0.0908 | +78.0% | [0.0542; 0.127] | 0.0019 | sim |
| matriz-filial2 | udp | 64 | perda_pct | 42.7 | 63.9 | +21.3 | +49.8% | [21.2; 21.3] | 3.42e-115 | sim |
| matriz-filial2 | udp | 64 | vazao_mbps | 5.16 | 3.24 | -1.91 | -37.1% | [-1.92; -1.91] | 1.27e-115 | sim |