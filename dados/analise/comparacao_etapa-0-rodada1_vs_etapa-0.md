# etapa-0 em relação a etapa-0-rodada1 (teste t de Welch, IC 95%, p ajustado por Holm)

| caminho | teste | tamanho (B) | métrica | média A | média B | diferença | dif. % | IC 95% da diferença | p (Holm) | significativa |
|---|---|---|---|---|---|---|---|---|---|---|
| LAN-matriz | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| LAN-matriz | latencia | — | rtt_medio_ms | 3.15 | 3.64 | +0.488 | +15.5% | [0.151; 0.825] | 1 | não |
| LAN-matriz | latencia | — | rtt_p95_ms | 4.7 | 4.75 | +0.0507 | +1.1% | [-0.224; 0.326] | 1 | não |
| LAN-matriz | tcp | — | retrans | 2.94e+03 | 2.95e+03 | +11.3 | +0.4% | [-63.6; 86.2] | 1 | não |
| LAN-matriz | tcp | — | vazao_mbps | 156 | 160 | +4.21 | +2.7% | [0.493; 7.93] | 1 | não |
| LAN-matriz | udp | 1024 | jitter_ms | 0.0264 | 0.0235 | -0.00292 | -11.0% | [-0.0123; 0.00651] | 1 | não |
| LAN-matriz | udp | 1024 | perda_pct | 16.4 | 18.7 | +2.36 | +14.4% | [-3.43; 8.14] | 1 | não |
| LAN-matriz | udp | 1024 | vazao_mbps | 75.2 | 73.1 | -2.12 | -2.8% | [-7.33; 3.09] | 1 | não |
| LAN-matriz | udp | 1400 | jitter_ms | 0.028 | 0.0551 | +0.0271 | +96.6% | [-0.0026; 0.0567] | 1 | não |
| LAN-matriz | udp | 1400 | perda_pct | 2.87 | 6.38 | +3.51 | +122.5% | [-3.11; 10.1] | 1 | não |
| LAN-matriz | udp | 1400 | vazao_mbps | 87.4 | 84.2 | -3.16 | -3.6% | [-9.12; 2.8] | 1 | não |
| LAN-matriz | udp | 512 | jitter_ms | 0.0245 | 0.0181 | -0.0064 | -26.1% | [-0.0135; 0.000717] | 1 | não |
| LAN-matriz | udp | 512 | perda_pct | 29.7 | 28.3 | -1.35 | -4.5% | [-3.47; 0.777] | 1 | não |
| LAN-matriz | udp | 512 | vazao_mbps | 63.3 | 62.1 | -1.19 | -1.9% | [-4.36; 1.99] | 1 | não |
| LAN-matriz | udp | 64 | jitter_ms | 0.0211 | 0.0126 | -0.0085 | -40.3% | [-0.0187; 0.00173] | 1 | não |
| LAN-matriz | udp | 64 | perda_pct | 86.6 | 85.8 | -0.846 | -1.0% | [-1.32; -0.377] | 0.199 | não |
| LAN-matriz | udp | 64 | vazao_mbps | 12 | 12.8 | +0.761 | +6.3% | [0.339; 1.18] | 0.199 | não |
| filial1-filial2 | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| filial1-filial2 | latencia | — | rtt_medio_ms | 87.8 | 89.6 | +1.85 | +2.1% | [1.05; 2.65] | 0.00708 | sim |
| filial1-filial2 | latencia | — | rtt_p95_ms | 91.1 | 91.7 | +0.577 | +0.6% | [-0.188; 1.34] | 1 | não |
| filial1-filial2 | tcp | — | retrans | 1.73 | 1.27 | -0.467 | -26.9% | [-3.58; 2.64] | 1 | não |
| filial1-filial2 | tcp | — | vazao_mbps | 9.11 | 9.29 | +0.185 | +2.0% | [-0.11; 0.48] | 1 | não |
| filial1-filial2 | udp | 1024 | jitter_ms | 0.352 | 0.323 | -0.0294 | -8.4% | [-0.0682; 0.00933] | 1 | não |
| filial1-filial2 | udp | 1024 | perda_pct | 0.0272 | 0.0342 | +0.00707 | +26.0% | [-0.0503; 0.0644] | 1 | não |
| filial1-filial2 | udp | 1024 | vazao_mbps | 9 | 9 | -0.0007 | -0.0% | [-0.00591; 0.00451] | 1 | não |
| filial1-filial2 | udp | 1400 | jitter_ms | 0.418 | 0.396 | -0.0217 | -5.2% | [-0.0813; 0.0378] | 1 | não |
| filial1-filial2 | udp | 1400 | perda_pct | 0.065 | 0.00243 | -0.0626 | -96.3% | [-0.179; 0.0538] | 1 | não |
| filial1-filial2 | udp | 1400 | vazao_mbps | 8.99 | 9 | +0.00553 | +0.1% | [-0.00495; 0.016] | 1 | não |
| filial1-filial2 | udp | 512 | jitter_ms | 0.277 | 0.241 | -0.0362 | -13.1% | [-0.0916; 0.0192] | 1 | não |
| filial1-filial2 | udp | 512 | perda_pct | 0.256 | 0.169 | -0.0867 | -33.9% | [-0.276; 0.102] | 1 | não |
| filial1-filial2 | udp | 512 | vazao_mbps | 8.98 | 8.98 | +0.00797 | +0.1% | [-0.00899; 0.0249] | 1 | não |
| filial1-filial2 | udp | 64 | jitter_ms | 0.0878 | 0.0916 | +0.0038 | +4.3% | [-0.00328; 0.0109] | 1 | não |
| filial1-filial2 | udp | 64 | perda_pct | 42.8 | 42.9 | +0.117 | +0.3% | [-0.282; 0.516] | 1 | não |
| filial1-filial2 | udp | 64 | vazao_mbps | 5.15 | 5.14 | -0.0105 | -0.2% | [-0.0464; 0.0254] | 1 | não |
| matriz-filial1 | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| matriz-filial1 | latencia | — | rtt_medio_ms | 27.3 | 29.5 | +2.25 | +8.3% | [1.39; 3.12] | 0.000881 | sim |
| matriz-filial1 | latencia | — | rtt_p95_ms | 31.2 | 32.5 | +1.31 | +4.2% | [0.336; 2.28] | 1 | não |
| matriz-filial1 | tcp | — | retrans | 30.4 | 5.17 | -25.2 | -83.0% | [-50.7; 0.246] | 1 | não |
| matriz-filial1 | tcp | — | vazao_mbps | 18.9 | 19 | +0.0715 | +0.4% | [-0.0156; 0.159] | 1 | não |
| matriz-filial1 | udp | 1024 | jitter_ms | 0.314 | 0.272 | -0.0421 | -13.4% | [-0.0914; 0.00717] | 1 | não |
| matriz-filial1 | udp | 1024 | perda_pct | 1.15 | 0.029 | -1.12 | -97.5% | [-1.73; -0.508] | 0.225 | não |
| matriz-filial1 | udp | 1024 | vazao_mbps | 17.8 | 18 | +0.201 | +1.1% | [0.0914; 0.311] | 0.226 | não |
| matriz-filial1 | udp | 1400 | jitter_ms | 0.275 | 0.335 | +0.0593 | +21.5% | [-0.0229; 0.142] | 1 | não |
| matriz-filial1 | udp | 1400 | perda_pct | 0.261 | 0.0191 | -0.241 | -92.7% | [-0.353; -0.13] | 0.0358 | sim |
| matriz-filial1 | udp | 1400 | vazao_mbps | 18 | 18 | +0.0436 | +0.2% | [0.0235; 0.0636] | 0.0344 | sim |
| matriz-filial1 | udp | 512 | jitter_ms | 0.368 | 0.312 | -0.0569 | -15.4% | [-0.118; 0.00375] | 1 | não |
| matriz-filial1 | udp | 512 | perda_pct | 7.76 | 2.95 | -4.81 | -62.0% | [-6.43; -3.2] | 0.00027 | sim |
| matriz-filial1 | udp | 512 | vazao_mbps | 16.6 | 17.5 | +0.867 | +5.2% | [0.575; 1.16] | 0.000269 | sim |
| matriz-filial1 | udp | 64 | jitter_ms | 0.0384 | 0.0992 | +0.0608 | +158.1% | [-0.0108; 0.132] | 1 | não |
| matriz-filial1 | udp | 64 | perda_pct | 68.9 | 64.1 | -4.81 | -7.0% | [-6.71; -2.9] | 0.0017 | sim |
| matriz-filial1 | udp | 64 | vazao_mbps | 5.59 | 6.46 | +0.865 | +15.5% | [0.522; 1.21] | 0.0017 | sim |
| matriz-filial2 | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| matriz-filial2 | latencia | — | rtt_medio_ms | 68.3 | 69.3 | +1.02 | +1.5% | [0.0654; 1.97] | 1 | não |
| matriz-filial2 | latencia | — | rtt_p95_ms | 71.6 | 71.9 | +0.257 | +0.4% | [-0.672; 1.19] | 1 | não |
| matriz-filial2 | tcp | — | retrans | 0 | 1.83 | +1.83 |  | [-0.231; 3.9] | 1 | não |
| matriz-filial2 | tcp | — | vazao_mbps | 9.32 | 9.32 | +0.0034 | +0.0% | [-0.00527; 0.0121] | 1 | não |
| matriz-filial2 | udp | 1024 | jitter_ms | 0.296 | 0.249 | -0.0478 | -16.1% | [-0.0821; -0.0135] | 1 | não |
| matriz-filial2 | udp | 1024 | perda_pct | 0.0479 | 0.00473 | -0.0431 | -90.1% | [-0.0866; 0.000313] | 1 | não |
| matriz-filial2 | udp | 1024 | vazao_mbps | 8.99 | 9 | +0.00367 | +0.0% | [-0.000213; 0.00755] | 1 | não |
| matriz-filial2 | udp | 1400 | jitter_ms | 0.301 | 0.285 | -0.0152 | -5.1% | [-0.0735; 0.043] | 1 | não |
| matriz-filial2 | udp | 1400 | perda_pct | 0.0561 | 0.0374 | -0.0187 | -33.4% | [-0.123; 0.0858] | 1 | não |
| matriz-filial2 | udp | 1400 | vazao_mbps | 8.99 | 9 | +0.00177 | +0.0% | [-0.00765; 0.0112] | 1 | não |
| matriz-filial2 | udp | 512 | jitter_ms | 0.251 | 0.192 | -0.0593 | -23.6% | [-0.141; 0.0224] | 1 | não |
| matriz-filial2 | udp | 512 | perda_pct | 0.221 | 0.127 | -0.0938 | -42.5% | [-0.247; 0.0588] | 1 | não |
| matriz-filial2 | udp | 512 | vazao_mbps | 8.98 | 8.99 | +0.00827 | +0.1% | [-0.00545; 0.022] | 1 | não |
| matriz-filial2 | udp | 64 | jitter_ms | 0.139 | 0.116 | -0.0229 | -16.5% | [-0.0647; 0.0189] | 1 | não |
| matriz-filial2 | udp | 64 | perda_pct | 43.2 | 42.7 | -0.554 | -1.3% | [-0.92; -0.188] | 1 | não |
| matriz-filial2 | udp | 64 | vazao_mbps | 5.11 | 5.16 | +0.0497 | +1.0% | [0.0168; 0.0826] | 1 | não |