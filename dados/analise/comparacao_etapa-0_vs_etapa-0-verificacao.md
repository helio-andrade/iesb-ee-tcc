# etapa-0-verificacao em relação a etapa-0 (teste t de Welch, IC 95%, p ajustado por Holm)

| caminho | teste | tamanho (B) | métrica | média A | média B | diferença | dif. % | IC 95% da diferença | p (Holm) | significativa |
|---|---|---|---|---|---|---|---|---|---|---|
| LAN-matriz | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| LAN-matriz | latencia | — | rtt_medio_ms | 3.64 | 3.54 | -0.0989 | -2.7% | [-0.42; 0.222] | 1 | não |
| LAN-matriz | latencia | — | rtt_p95_ms | 4.75 | 4.76 | +0.0137 | +0.3% | [-0.198; 0.226] | 1 | não |
| LAN-matriz | tcp | — | retrans | 2.95e+03 | 2.92e+03 | -29.6 | -1.0% | [-111; 51.4] | 1 | não |
| LAN-matriz | tcp | — | vazao_mbps | 160 | 161 | +0.667 | +0.4% | [-3.38; 4.71] | 1 | não |
| LAN-matriz | udp | 1024 | jitter_ms | 0.0235 | 0.0416 | +0.0181 | +76.9% | [-0.0172; 0.0534] | 1 | não |
| LAN-matriz | udp | 1024 | perda_pct | 18.7 | 16.3 | -2.44 | -13.0% | [-8.23; 3.34] | 1 | não |
| LAN-matriz | udp | 1024 | vazao_mbps | 73.1 | 75.3 | +2.2 | +3.0% | [-3; 7.4] | 1 | não |
| LAN-matriz | udp | 1400 | jitter_ms | 0.0551 | 0.027 | -0.0281 | -51.0% | [-0.0581; 0.00186] | 1 | não |
| LAN-matriz | udp | 1400 | perda_pct | 6.38 | 3.92 | -2.46 | -38.6% | [-9.51; 4.58] | 1 | não |
| LAN-matriz | udp | 1400 | vazao_mbps | 84.2 | 86.5 | +2.22 | +2.6% | [-4.12; 8.56] | 1 | não |
| LAN-matriz | udp | 512 | jitter_ms | 0.0181 | 0.0128 | -0.00533 | -29.4% | [-0.0113; 0.000627] | 1 | não |
| LAN-matriz | udp | 512 | perda_pct | 28.3 | 29.4 | +1.08 | +3.8% | [-1.44; 3.6] | 1 | não |
| LAN-matriz | udp | 512 | vazao_mbps | 62.1 | 63.5 | +1.43 | +2.3% | [-1.94; 4.8] | 1 | não |
| LAN-matriz | udp | 64 | jitter_ms | 0.0126 | 0.0542 | +0.0416 | +331.3% | [-0.0612; 0.144] | 1 | não |
| LAN-matriz | udp | 64 | perda_pct | 85.8 | 86 | +0.226 | +0.3% | [-0.763; 1.21] | 1 | não |
| LAN-matriz | udp | 64 | vazao_mbps | 12.8 | 12.6 | -0.203 | -1.6% | [-1.09; 0.686] | 1 | não |
| filial1-filial2 | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| filial1-filial2 | latencia | — | rtt_medio_ms | 89.6 | 89.1 | -0.57 | -0.6% | [-1.53; 0.387] | 1 | não |
| filial1-filial2 | latencia | — | rtt_p95_ms | 91.7 | 91.9 | +0.193 | +0.2% | [-0.581; 0.968] | 1 | não |
| filial1-filial2 | tcp | — | retrans | 1.27 | 0 | -1.27 | -100.0% | [-3.86; 1.32] | 1 | não |
| filial1-filial2 | tcp | — | vazao_mbps | 9.29 | 9.32 | +0.0275 | +0.3% | [-0.00687; 0.0619] | 1 | não |
| filial1-filial2 | udp | 1024 | jitter_ms | 0.323 | 0.313 | -0.00977 | -3.0% | [-0.115; 0.0957] | 1 | não |
| filial1-filial2 | udp | 1024 | perda_pct | 0.0342 | 0.078 | +0.0438 | +127.8% | [-0.169; 0.256] | 1 | não |
| filial1-filial2 | udp | 1024 | vazao_mbps | 9 | 8.99 | -0.00357 | -0.0% | [-0.0226; 0.0155] | 1 | não |
| filial1-filial2 | udp | 1400 | jitter_ms | 0.396 | 0.336 | -0.0605 | -15.3% | [-0.126; 0.00464] | 1 | não |
| filial1-filial2 | udp | 1400 | perda_pct | 0.00243 | 0.039 | +0.0366 | +1502.7% | [-0.0716; 0.145] | 1 | não |
| filial1-filial2 | udp | 1400 | vazao_mbps | 9 | 9 | -0.00347 | -0.0% | [-0.0132; 0.00626] | 1 | não |
| filial1-filial2 | udp | 512 | jitter_ms | 0.241 | 0.172 | -0.0694 | -28.8% | [-0.169; 0.0301] | 1 | não |
| filial1-filial2 | udp | 512 | perda_pct | 0.169 | 0.0224 | -0.146 | -86.7% | [-0.286; -0.00688] | 1 | não |
| filial1-filial2 | udp | 512 | vazao_mbps | 8.98 | 9 | +0.0131 | +0.1% | [0.000559; 0.0256] | 1 | não |
| filial1-filial2 | udp | 64 | jitter_ms | 0.0916 | 0.0806 | -0.011 | -12.0% | [-0.0233; 0.00135] | 1 | não |
| filial1-filial2 | udp | 64 | perda_pct | 42.9 | 42.8 | -0.0455 | -0.1% | [-0.589; 0.498] | 1 | não |
| filial1-filial2 | udp | 64 | vazao_mbps | 5.14 | 5.14 | +0.00443 | +0.1% | [-0.0448; 0.0536] | 1 | não |
| matriz-filial1 | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| matriz-filial1 | latencia | — | rtt_medio_ms | 29.5 | 28.5 | -1 | -3.4% | [-2.38; 0.375] | 1 | não |
| matriz-filial1 | latencia | — | rtt_p95_ms | 32.5 | 31.8 | -0.647 | -2.0% | [-2.68; 1.39] | 1 | não |
| matriz-filial1 | tcp | — | retrans | 5.17 | 96.8 | +91.6 | +1773.5% | [-176; 360] | 1 | não |
| matriz-filial1 | tcp | — | vazao_mbps | 19 | 19 | +0.0004 | +0.0% | [-0.022; 0.0228] | 1 | não |
| matriz-filial1 | udp | 1024 | jitter_ms | 0.272 | 0.309 | +0.0369 | +13.6% | [-0.0638; 0.138] | 1 | não |
| matriz-filial1 | udp | 1024 | perda_pct | 0.029 | 0.0036 | -0.0254 | -87.6% | [-0.0505; -0.000198] | 1 | não |
| matriz-filial1 | udp | 1024 | vazao_mbps | 18 | 18 | +0.00447 | +0.0% | [-3.53e-05; 0.00897] | 1 | não |
| matriz-filial1 | udp | 1400 | jitter_ms | 0.335 | 0.287 | -0.0477 | -14.3% | [-0.166; 0.0709] | 1 | não |
| matriz-filial1 | udp | 1400 | perda_pct | 0.0191 | 0.0586 | +0.0395 | +206.8% | [-0.122; 0.201] | 1 | não |
| matriz-filial1 | udp | 1400 | vazao_mbps | 18 | 18 | -0.00743 | -0.0% | [-0.037; 0.0221] | 1 | não |
| matriz-filial1 | udp | 512 | jitter_ms | 0.312 | 0.316 | +0.004 | +1.3% | [-0.0775; 0.0855] | 1 | não |
| matriz-filial1 | udp | 512 | perda_pct | 2.95 | 3.45 | +0.504 | +17.1% | [-2.32; 3.33] | 1 | não |
| matriz-filial1 | udp | 512 | vazao_mbps | 17.5 | 17.4 | -0.0909 | -0.5% | [-0.599; 0.417] | 1 | não |
| matriz-filial1 | udp | 64 | jitter_ms | 0.0992 | 0.042 | -0.0572 | -57.7% | [-0.135; 0.0208] | 1 | não |
| matriz-filial1 | udp | 64 | perda_pct | 64.1 | 67 | +2.83 | +4.4% | [-1.08; 6.75] | 1 | não |
| matriz-filial1 | udp | 64 | vazao_mbps | 6.46 | 5.95 | -0.51 | -7.9% | [-1.21; 0.195] | 1 | não |
| matriz-filial2 | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| matriz-filial2 | latencia | — | rtt_medio_ms | 69.3 | 69.8 | +0.531 | +0.8% | [-0.349; 1.41] | 1 | não |
| matriz-filial2 | latencia | — | rtt_p95_ms | 71.9 | 72.9 | +0.983 | +1.4% | [0.158; 1.81] | 1 | não |
| matriz-filial2 | tcp | — | retrans | 1.83 | 0 | -1.83 | -100.0% | [-3.9; 0.231] | 1 | não |
| matriz-filial2 | tcp | — | vazao_mbps | 9.32 | 9.32 | -0.0041 | -0.0% | [-0.0128; 0.00459] | 1 | não |
| matriz-filial2 | udp | 1024 | jitter_ms | 0.249 | 0.309 | +0.0605 | +24.3% | [-0.0149; 0.136] | 1 | não |
| matriz-filial2 | udp | 1024 | perda_pct | 0.00473 | 0 | -0.00473 | -100.0% | [-0.0144; 0.00495] | 1 | não |
| matriz-filial2 | udp | 1024 | vazao_mbps | 9 | 9 | +0.000267 | +0.0% | [-0.000999; 0.00153] | 1 | não |
| matriz-filial2 | udp | 1400 | jitter_ms | 0.285 | 0.482 | +0.196 | +68.8% | [-0.374; 0.767] | 1 | não |
| matriz-filial2 | udp | 1400 | perda_pct | 0.0374 | 0.649 | +0.611 | +1636.3% | [-1.17; 2.4] | 1 | não |
| matriz-filial2 | udp | 1400 | vazao_mbps | 9 | 8.94 | -0.0548 | -0.6% | [-0.215; 0.106] | 1 | não |
| matriz-filial2 | udp | 512 | jitter_ms | 0.192 | 0.165 | -0.0263 | -13.7% | [-0.0934; 0.0409] | 1 | não |
| matriz-filial2 | udp | 512 | perda_pct | 0.127 | 0.0654 | -0.0617 | -48.5% | [-0.25; 0.127] | 1 | não |
| matriz-filial2 | udp | 512 | vazao_mbps | 8.99 | 8.99 | +0.0059 | +0.1% | [-0.0106; 0.0224] | 1 | não |
| matriz-filial2 | udp | 64 | jitter_ms | 0.116 | 0.152 | +0.0359 | +30.9% | [-0.0773; 0.149] | 1 | não |
| matriz-filial2 | udp | 64 | perda_pct | 42.7 | 42.8 | +0.0697 | +0.2% | [-0.258; 0.397] | 1 | não |
| matriz-filial2 | udp | 64 | vazao_mbps | 5.16 | 5.15 | -0.00657 | -0.1% | [-0.0362; 0.0231] | 1 | não |