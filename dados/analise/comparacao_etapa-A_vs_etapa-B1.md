# etapa-B1 em relação a etapa-A (teste t de Welch, IC 95%, p ajustado por Holm)

| caminho | teste | tamanho (B) | métrica | média A | média B | diferença | dif. % | IC 95% da diferença | p (Holm) | significativa |
|---|---|---|---|---|---|---|---|---|---|---|
| LAN-matriz | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| LAN-matriz | latencia | — | rtt_medio_ms | 3.97 | 5.15 | +1.18 | +29.8% | [0.606; 1.76] | 0.0526 | não |
| LAN-matriz | latencia | — | rtt_p95_ms | 5.16 | 7.39 | +2.23 | +43.2% | [1.6; 2.86] | 8.78e-06 | sim |
| LAN-matriz | tcp | — | retrans | 2.8e+03 | 1.5e+03 | -1.3e+03 | -46.5% | [-1.36e+03; -1.24e+03] | 4.01e-35 | sim |
| LAN-matriz | tcp | — | vazao_mbps | 143 | 79 | -63.6 | -44.6% | [-65.3; -61.9] | 1.99e-53 | sim |
| LAN-matriz | udp | 1024 | jitter_ms | 0.0411 | 0.0652 | +0.0241 | +58.6% | [-0.00205; 0.0502] | 1 | não |
| LAN-matriz | udp | 1024 | perda_pct | 20.8 | 20.1 | -0.627 | -3.0% | [-6.4; 5.15] | 1 | não |
| LAN-matriz | udp | 1024 | vazao_mbps | 71.3 | 71.9 | +0.563 | +0.8% | [-4.63; 5.76] | 1 | não |
| LAN-matriz | udp | 1400 | jitter_ms | 0.0499 | 0.0596 | +0.00964 | +19.3% | [-0.0158; 0.0351] | 1 | não |
| LAN-matriz | udp | 1400 | perda_pct | 7.31 | 6.38 | -0.923 | -12.6% | [-7.62; 5.77] | 1 | não |
| LAN-matriz | udp | 1400 | vazao_mbps | 83.4 | 84.2 | +0.83 | +1.0% | [-5.2; 6.86] | 1 | não |
| LAN-matriz | udp | 512 | jitter_ms | 0.0319 | 0.0917 | +0.0598 | +187.7% | [0.0345; 0.0851] | 0.0103 | sim |
| LAN-matriz | udp | 512 | perda_pct | 32.1 | 48.5 | +16.4 | +50.9% | [11.5; 21.2] | 3.59e-05 | sim |
| LAN-matriz | udp | 512 | vazao_mbps | 61.1 | 46.4 | -14.7 | -24.1% | [-19.1; -10.3] | 3.59e-05 | sim |
| LAN-matriz | udp | 64 | jitter_ms | 0.0245 | 0.182 | +0.157 | +641.8% | [0.0534; 0.261] | 1 | não |
| LAN-matriz | udp | 64 | perda_pct | 85.7 | 95.5 | +9.74 | +11.4% | [3.67; 15.8] | 0.725 | não |
| LAN-matriz | udp | 64 | vazao_mbps | 10.4 | 4.07 | -6.36 | -61.0% | [-7.07; -5.65] | 3.84e-22 | sim |
| filial1-filial2 | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| filial1-filial2 | latencia | — | rtt_medio_ms | 89.4 | 88.3 | -1.09 | -1.2% | [-2.01; -0.168] | 1 | não |
| filial1-filial2 | latencia | — | rtt_p95_ms | 91.8 | 90.7 | -1.08 | -1.2% | [-2.12; -0.0498] | 1 | não |
| filial1-filial2 | tcp | — | retrans | 3.07 | 2.97 | -0.1 | -3.3% | [-5.46; 5.26] | 1 | não |
| filial1-filial2 | tcp | — | vazao_mbps | 9.06 | 9.3 | +0.234 | +2.6% | [-0.0827; 0.55] | 1 | não |
| filial1-filial2 | udp | 1024 | jitter_ms | 0.312 | 0.362 | +0.0504 | +16.2% | [0.0158; 0.0849] | 1 | não |
| filial1-filial2 | udp | 1024 | perda_pct | 0.0597 | 0.114 | +0.0542 | +90.9% | [-0.0929; 0.201] | 1 | não |
| filial1-filial2 | udp | 1024 | vazao_mbps | 8.99 | 8.99 | -0.005 | -0.1% | [-0.0182; 0.00819] | 1 | não |
| filial1-filial2 | udp | 1400 | jitter_ms | 0.387 | 0.415 | +0.0277 | +7.2% | [-0.0118; 0.0672] | 1 | não |
| filial1-filial2 | udp | 1400 | perda_pct | 0.0732 | 0.0114 | -0.0618 | -84.4% | [-0.184; 0.0602] | 1 | não |
| filial1-filial2 | udp | 1400 | vazao_mbps | 8.99 | 9 | +0.0056 | +0.1% | [-0.00535; 0.0165] | 1 | não |
| filial1-filial2 | udp | 512 | jitter_ms | 0.212 | 0.219 | +0.00663 | +3.1% | [-0.031; 0.0442] | 1 | não |
| filial1-filial2 | udp | 512 | perda_pct | 0.049 | 0.206 | +0.157 | +321.1% | [-0.0155; 0.33] | 1 | não |
| filial1-filial2 | udp | 512 | vazao_mbps | 8.99 | 8.98 | -0.0141 | -0.2% | [-0.0296; 0.00149] | 1 | não |
| filial1-filial2 | udp | 64 | jitter_ms | 0.0871 | 0.112 | +0.0248 | +28.5% | [0.00365; 0.046] | 1 | não |
| filial1-filial2 | udp | 64 | perda_pct | 42.7 | 42.6 | -0.00563 | -0.0% | [-0.0814; 0.0702] | 1 | não |
| filial1-filial2 | udp | 64 | vazao_mbps | 5.16 | 5.16 | +0.0006 | +0.0% | [-0.00623; 0.00743] | 1 | não |
| matriz-filial1 | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| matriz-filial1 | latencia | — | rtt_medio_ms | 29.5 | 27.5 | -2.02 | -6.8% | [-3.1; -0.941] | 0.117 | não |
| matriz-filial1 | latencia | — | rtt_p95_ms | 32.2 | 30.2 | -2.01 | -6.2% | [-3.32; -0.703] | 0.854 | não |
| matriz-filial1 | tcp | — | retrans | 0.733 | 13.1 | +12.4 | +1690.9% | [-1.55; 26.3] | 1 | não |
| matriz-filial1 | tcp | — | vazao_mbps | 19 | 19 | +0.0152 | +0.1% | [-0.027; 0.0574] | 1 | não |
| matriz-filial1 | udp | 1024 | jitter_ms | 0.324 | 0.272 | -0.0514 | -15.9% | [-0.161; 0.058] | 1 | não |
| matriz-filial1 | udp | 1024 | perda_pct | 0.191 | 0.13 | -0.0616 | -32.2% | [-0.256; 0.132] | 1 | não |
| matriz-filial1 | udp | 1024 | vazao_mbps | 18 | 18 | +0.0109 | +0.1% | [-0.0241; 0.0458] | 1 | não |
| matriz-filial1 | udp | 1400 | jitter_ms | 0.267 | 0.302 | +0.0356 | +13.3% | [-0.0608; 0.132] | 1 | não |
| matriz-filial1 | udp | 1400 | perda_pct | 0.1 | 0.257 | +0.157 | +155.8% | [-0.0675; 0.381] | 1 | não |
| matriz-filial1 | udp | 1400 | vazao_mbps | 18 | 18 | -0.028 | -0.2% | [-0.0683; 0.0123] | 1 | não |
| matriz-filial1 | udp | 512 | jitter_ms | 0.326 | 0.343 | +0.0166 | +5.1% | [-0.0129; 0.0462] | 1 | não |
| matriz-filial1 | udp | 512 | perda_pct | 4.95 | 7.94 | +2.99 | +60.3% | [1.95; 4.03] | 0.000136 | sim |
| matriz-filial1 | udp | 512 | vazao_mbps | 17.1 | 16.6 | -0.537 | -3.1% | [-0.725; -0.35] | 0.000138 | sim |
| matriz-filial1 | udp | 64 | jitter_ms | 0.0456 | 0.12 | +0.0743 | +162.9% | [0.028; 0.121] | 0.703 | não |
| matriz-filial1 | udp | 64 | perda_pct | 67.7 | 65.3 | -2.46 | -3.6% | [-3.72; -1.2] | 0.0801 | não |
| matriz-filial1 | udp | 64 | vazao_mbps | 5.81 | 6.25 | +0.443 | +7.6% | [0.216; 0.669] | 0.0799 | não |
| matriz-filial2 | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| matriz-filial2 | latencia | — | rtt_medio_ms | 69.8 | 68 | -1.83 | -2.6% | [-2.86; -0.801] | 0.217 | não |
| matriz-filial2 | latencia | — | rtt_p95_ms | 72.2 | 70.9 | -1.29 | -1.8% | [-2.38; -0.205] | 1 | não |
| matriz-filial2 | tcp | — | retrans | 2.33 | 0.7 | -1.63 | -70.0% | [-5.44; 2.18] | 1 | não |
| matriz-filial2 | tcp | — | vazao_mbps | 9.32 | 9.33 | +0.00523 | +0.1% | [-0.00421; 0.0147] | 1 | não |
| matriz-filial2 | udp | 1024 | jitter_ms | 0.345 | 0.246 | -0.0995 | -28.8% | [-0.223; 0.0241] | 1 | não |
| matriz-filial2 | udp | 1024 | perda_pct | 0.0502 | 0.00413 | -0.046 | -91.8% | [-0.091; -0.00111] | 1 | não |
| matriz-filial2 | udp | 1024 | vazao_mbps | 8.99 | 9 | +0.00453 | +0.1% | [0.000464; 0.0086] | 1 | não |
| matriz-filial2 | udp | 1400 | jitter_ms | 0.289 | 0.28 | -0.0088 | -3.0% | [-0.0626; 0.045] | 1 | não |
| matriz-filial2 | udp | 1400 | perda_pct | 0.0122 | 0.0382 | +0.026 | +214.0% | [-0.0482; 0.1] | 1 | não |
| matriz-filial2 | udp | 1400 | vazao_mbps | 9 | 9 | -0.00223 | -0.0% | [-0.00893; 0.00446] | 1 | não |
| matriz-filial2 | udp | 512 | jitter_ms | 0.19 | 0.171 | -0.0191 | -10.0% | [-0.0777; 0.0396] | 1 | não |
| matriz-filial2 | udp | 512 | perda_pct | 0.122 | 0.22 | +0.0979 | +80.5% | [-0.103; 0.299] | 1 | não |
| matriz-filial2 | udp | 512 | vazao_mbps | 8.99 | 8.98 | -0.00907 | -0.1% | [-0.0272; 0.00909] | 1 | não |
| matriz-filial2 | udp | 64 | jitter_ms | 0.123 | 0.139 | +0.0157 | +12.8% | [-0.024; 0.0554] | 1 | não |
| matriz-filial2 | udp | 64 | perda_pct | 42.8 | 42.7 | -0.117 | -0.3% | [-0.258; 0.0247] | 1 | não |
| matriz-filial2 | udp | 64 | vazao_mbps | 5.15 | 5.16 | +0.0105 | +0.2% | [-0.00216; 0.0232] | 1 | não |