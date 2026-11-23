# etapa-B2-teste em relação a etapa-B1 (teste t de Welch, IC 95%, p ajustado por Holm)

| caminho | teste | tamanho (B) | métrica | média A | média B | diferença | dif. % | IC 95% da diferença | p (Holm) | significativa |
|---|---|---|---|---|---|---|---|---|---|---|
| LAN-matriz | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| LAN-matriz | latencia | — | rtt_medio_ms | 5.15 | 6.68 | +1.53 | +29.7% | [0.826; 2.24] | 0.0172 | sim |
| LAN-matriz | latencia | — | rtt_p95_ms | 7.39 | 8.62 | +1.23 | +16.6% | [0.508; 1.95] | 0.335 | não |
| LAN-matriz | tcp | — | retrans | 1.5e+03 | 1.54e+03 | +44.8 | +3.0% | [-0.865; 90.5] | 1 | não |
| LAN-matriz | tcp | — | vazao_mbps | 79 | 80.6 | +1.58 | +2.0% | [-0.93; 4.08] | 1 | não |
| LAN-matriz | udp | 1024 | jitter_ms | 0.0652 | 0.0663 | +0.00107 | +1.6% | [-0.0419; 0.0441] | 1 | não |
| LAN-matriz | udp | 1024 | perda_pct | 20.1 | 19.3 | -0.855 | -4.2% | [-2.5; 0.788] | 1 | não |
| LAN-matriz | udp | 1024 | vazao_mbps | 71.9 | 72.6 | +0.771 | +1.1% | [-0.708; 2.25] | 1 | não |
| LAN-matriz | udp | 1400 | jitter_ms | 0.0596 | 0.0502 | -0.00933 | -15.7% | [-0.0335; 0.0149] | 1 | não |
| LAN-matriz | udp | 1400 | perda_pct | 6.38 | 5.34 | -1.04 | -16.3% | [-2.75; 0.667] | 1 | não |
| LAN-matriz | udp | 1400 | vazao_mbps | 84.2 | 85.2 | +0.937 | +1.1% | [-0.601; 2.47] | 1 | não |
| LAN-matriz | udp | 512 | jitter_ms | 0.0917 | 0.0856 | -0.0061 | -6.7% | [-0.0378; 0.0256] | 1 | não |
| LAN-matriz | udp | 512 | perda_pct | 48.5 | 46.5 | -1.96 | -4.0% | [-3.14; -0.781] | 0.422 | não |
| LAN-matriz | udp | 512 | vazao_mbps | 46.4 | 48.1 | +1.76 | +3.8% | [0.702; 2.82] | 0.423 | não |
| LAN-matriz | udp | 64 | jitter_ms | 0.182 | 0.371 | +0.189 | +104.0% | [0.0107; 0.368] | 1 | não |
| LAN-matriz | udp | 64 | perda_pct | 95.5 | 96 | +0.494 | +0.5% | [-0.251; 1.24] | 1 | não |
| LAN-matriz | udp | 64 | vazao_mbps | 4.07 | 3.62 | -0.444 | -10.9% | [-1.11; 0.226] | 1 | não |
| filial1-filial2 | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| filial1-filial2 | latencia | — | rtt_medio_ms | 88.3 | 94.1 | +5.78 | +6.5% | [4.6; 6.97] | 5.45e-11 | sim |
| filial1-filial2 | latencia | — | rtt_p95_ms | 90.7 | 96.7 | +5.99 | +6.6% | [4.73; 7.24] | 5.5e-11 | sim |
| filial1-filial2 | tcp | — | retrans | 2.97 | 4.67 | +1.7 | +57.3% | [-4.62; 8.02] | 1 | não |
| filial1-filial2 | tcp | — | vazao_mbps | 9.3 | 8.92 | -0.38 | -4.1% | [-0.398; -0.362] | 1.07e-31 | sim |
| filial1-filial2 | udp | 1024 | jitter_ms | 0.362 | 0.437 | +0.0748 | +20.7% | [-0.0438; 0.193] | 1 | não |
| filial1-filial2 | udp | 1024 | perda_pct | 0.114 | 0.0873 | -0.0266 | -23.3% | [-0.2; 0.147] | 1 | não |
| filial1-filial2 | udp | 1024 | vazao_mbps | 8.99 | 8.99 | +0.00253 | +0.0% | [-0.013; 0.0181] | 1 | não |
| filial1-filial2 | udp | 1400 | jitter_ms | 0.415 | 0.411 | -0.00343 | -0.8% | [-0.0429; 0.036] | 1 | não |
| filial1-filial2 | udp | 1400 | perda_pct | 0.0114 | 0.12 | +0.108 | +948.2% | [-0.0459; 0.262] | 1 | não |
| filial1-filial2 | udp | 1400 | vazao_mbps | 9 | 8.99 | -0.0096 | -0.1% | [-0.0235; 0.00429] | 1 | não |
| filial1-filial2 | udp | 512 | jitter_ms | 0.219 | 0.51 | +0.291 | +132.6% | [0.253; 0.328] | 1.45e-19 | sim |
| filial1-filial2 | udp | 512 | perda_pct | 0.206 | 0.193 | -0.0134 | -6.5% | [-0.22; 0.194] | 1 | não |
| filial1-filial2 | udp | 512 | vazao_mbps | 8.98 | 8.98 | +0.00107 | +0.0% | [-0.0175; 0.0197] | 1 | não |
| filial1-filial2 | udp | 64 | jitter_ms | 0.112 | 0.179 | +0.0675 | +60.3% | [0.0368; 0.0982] | 0.0145 | sim |
| filial1-filial2 | udp | 64 | perda_pct | 42.6 | 60.8 | +18.2 | +42.7% | [18.1; 18.3] | 4.15e-52 | sim |
| filial1-filial2 | udp | 64 | vazao_mbps | 5.16 | 3.52 | -1.64 | -31.7% | [-1.65; -1.63] | 3.75e-52 | sim |
| matriz-filial1 | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| matriz-filial1 | latencia | — | rtt_medio_ms | 27.5 | 29.9 | +2.43 | +8.8% | [1.38; 3.47] | 0.00634 | sim |
| matriz-filial1 | latencia | — | rtt_p95_ms | 30.2 | 32.6 | +2.43 | +8.0% | [1.07; 3.79] | 0.203 | não |
| matriz-filial1 | tcp | — | retrans | 13.1 | 1.9 | -11.2 | -85.5% | [-25.3; 2.82] | 1 | não |
| matriz-filial1 | tcp | — | vazao_mbps | 19 | 18.2 | -0.777 | -4.1% | [-0.789; -0.765] | 3.3e-46 | sim |
| matriz-filial1 | udp | 1024 | jitter_ms | 0.272 | 0.362 | +0.0902 | +33.1% | [0.0379; 0.142] | 0.299 | não |
| matriz-filial1 | udp | 1024 | perda_pct | 0.13 | 0.802 | +0.672 | +518.5% | [0.0825; 1.26] | 1 | não |
| matriz-filial1 | udp | 1024 | vazao_mbps | 18 | 17.9 | -0.121 | -0.7% | [-0.227; -0.0149] | 1 | não |
| matriz-filial1 | udp | 1400 | jitter_ms | 0.302 | 0.372 | +0.07 | +23.1% | [-0.107; 0.247] | 1 | não |
| matriz-filial1 | udp | 1400 | perda_pct | 0.257 | 0.105 | -0.152 | -59.2% | [-0.389; 0.0849] | 1 | não |
| matriz-filial1 | udp | 1400 | vazao_mbps | 18 | 18 | +0.0272 | +0.2% | [-0.0154; 0.0698] | 1 | não |
| matriz-filial1 | udp | 512 | jitter_ms | 0.343 | 0.347 | +0.0047 | +1.4% | [-0.0179; 0.0273] | 1 | não |
| matriz-filial1 | udp | 512 | perda_pct | 7.94 | 6.55 | -1.39 | -17.5% | [-2.55; -0.23] | 1 | não |
| matriz-filial1 | udp | 512 | vazao_mbps | 16.6 | 16.8 | +0.251 | +1.5% | [0.0413; 0.46] | 1 | não |
| matriz-filial1 | udp | 64 | jitter_ms | 0.12 | 0.0948 | -0.0251 | -20.9% | [-0.0755; 0.0253] | 1 | não |
| matriz-filial1 | udp | 64 | perda_pct | 65.3 | 68.3 | +3.08 | +4.7% | [2.17; 3.99] | 2.35e-06 | sim |
| matriz-filial1 | udp | 64 | vazao_mbps | 6.25 | 5.7 | -0.554 | -8.9% | [-0.718; -0.39] | 2.35e-06 | sim |
| matriz-filial2 | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| matriz-filial2 | latencia | — | rtt_medio_ms | 68 | 70.7 | +2.7 | +4.0% | [1.77; 3.64] | 9.5e-05 | sim |
| matriz-filial2 | latencia | — | rtt_p95_ms | 70.9 | 73.2 | +2.31 | +3.3% | [1.19; 3.44] | 0.0378 | sim |
| matriz-filial2 | tcp | — | retrans | 0.7 | 3.8 | +3.1 | +442.9% | [-0.382; 6.58] | 1 | não |
| matriz-filial2 | tcp | — | vazao_mbps | 9.33 | 8.77 | -0.554 | -5.9% | [-0.871; -0.236] | 0.351 | não |
| matriz-filial2 | udp | 1024 | jitter_ms | 0.246 | 0.294 | +0.0485 | +19.7% | [-0.0156; 0.113] | 1 | não |
| matriz-filial2 | udp | 1024 | perda_pct | 0.00413 | 0.0874 | +0.0833 | +2014.5% | [-0.0173; 0.184] | 1 | não |
| matriz-filial2 | udp | 1024 | vazao_mbps | 9 | 8.99 | -0.00773 | -0.1% | [-0.0168; 0.00131] | 1 | não |
| matriz-filial2 | udp | 1400 | jitter_ms | 0.28 | 0.245 | -0.0356 | -12.7% | [-0.0845; 0.0132] | 1 | não |
| matriz-filial2 | udp | 1400 | perda_pct | 0.0382 | 0.137 | +0.0984 | +257.5% | [-0.0563; 0.253] | 1 | não |
| matriz-filial2 | udp | 1400 | vazao_mbps | 9 | 8.99 | -0.00893 | -0.1% | [-0.0229; 0.00508] | 1 | não |
| matriz-filial2 | udp | 512 | jitter_ms | 0.171 | 0.504 | +0.334 | +195.4% | [0.296; 0.371] | 2.04e-21 | sim |
| matriz-filial2 | udp | 512 | perda_pct | 0.22 | 0.168 | -0.0517 | -23.5% | [-0.257; 0.154] | 1 | não |
| matriz-filial2 | udp | 512 | vazao_mbps | 8.98 | 8.98 | +0.0046 | +0.1% | [-0.0139; 0.0231] | 1 | não |
| matriz-filial2 | udp | 64 | jitter_ms | 0.139 | 0.235 | +0.096 | +69.0% | [0.0467; 0.145] | 0.0849 | não |
| matriz-filial2 | udp | 64 | perda_pct | 42.7 | 65.1 | +22.4 | +52.5% | [20; 24.9] | 3.67e-15 | sim |
| matriz-filial2 | udp | 64 | vazao_mbps | 5.16 | 3.14 | -2.02 | -39.1% | [-2.24; -1.8] | 3.67e-15 | sim |