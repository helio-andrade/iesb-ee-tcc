# etapa-B1 em relação a etapa-0 (teste t de Welch, IC 95%, p ajustado por Holm)

| caminho | teste | tamanho (B) | métrica | média A | média B | diferença | dif. % | IC 95% da diferença | p (Holm) | significativa |
|---|---|---|---|---|---|---|---|---|---|---|
| LAN-matriz | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| LAN-matriz | latencia | — | rtt_medio_ms | 3.64 | 5.15 | +1.51 | +41.6% | [0.929; 2.1] | 0.00145 | sim |
| LAN-matriz | latencia | — | rtt_p95_ms | 4.75 | 7.39 | +2.65 | +55.8% | [2.01; 3.28] | 1.85e-07 | sim |
| LAN-matriz | tcp | — | retrans | 2.95e+03 | 1.5e+03 | -1.45e+03 | -49.2% | [-1.52e+03; -1.38e+03] | 1.13e-33 | sim |
| LAN-matriz | tcp | — | vazao_mbps | 160 | 79 | -81.4 | -50.8% | [-84.7; -78.2] | 2.7e-32 | sim |
| LAN-matriz | udp | 1024 | jitter_ms | 0.0235 | 0.0652 | +0.0417 | +177.4% | [0.0168; 0.0666] | 0.355 | não |
| LAN-matriz | udp | 1024 | perda_pct | 18.7 | 20.1 | +1.41 | +7.5% | [-4.52; 7.34] | 1 | não |
| LAN-matriz | udp | 1024 | vazao_mbps | 73.1 | 71.9 | -1.27 | -1.7% | [-6.6; 4.07] | 1 | não |
| LAN-matriz | udp | 1400 | jitter_ms | 0.0551 | 0.0596 | +0.00446 | +8.1% | [-0.0302; 0.0391] | 1 | não |
| LAN-matriz | udp | 1400 | perda_pct | 6.38 | 6.38 | +0.00333 | +0.1% | [-6.77; 6.77] | 1 | não |
| LAN-matriz | udp | 1400 | vazao_mbps | 84.2 | 84.2 | -0.00237 | -0.0% | [-6.09; 6.09] | 1 | não |
| LAN-matriz | udp | 512 | jitter_ms | 0.0181 | 0.0917 | +0.0735 | +405.5% | [0.0486; 0.0984] | 0.000361 | sim |
| LAN-matriz | udp | 512 | perda_pct | 28.3 | 48.5 | +20.1 | +71.0% | [17.9; 22.4] | 1.07e-18 | sim |
| LAN-matriz | udp | 512 | vazao_mbps | 62.1 | 46.4 | -15.7 | -25.3% | [-18.9; -12.5] | 6.16e-09 | sim |
| LAN-matriz | udp | 64 | jitter_ms | 0.0126 | 0.182 | +0.169 | +1348.3% | [0.0656; 0.273] | 0.473 | não |
| LAN-matriz | udp | 64 | perda_pct | 85.8 | 95.5 | +9.69 | +11.3% | [9.14; 10.3] | 1.58e-30 | sim |
| LAN-matriz | udp | 64 | vazao_mbps | 12.8 | 4.07 | -8.72 | -68.2% | [-9.22; -8.22] | 1.58e-30 | sim |
| filial1-filial2 | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| filial1-filial2 | latencia | — | rtt_medio_ms | 89.6 | 88.3 | -1.31 | -1.5% | [-2.24; -0.371] | 1 | não |
| filial1-filial2 | latencia | — | rtt_p95_ms | 91.7 | 90.7 | -0.92 | -1.0% | [-1.94; 0.103] | 1 | não |
| filial1-filial2 | tcp | — | retrans | 1.27 | 2.97 | +1.7 | +134.2% | [-2.75; 6.15] | 1 | não |
| filial1-filial2 | tcp | — | vazao_mbps | 9.29 | 9.3 | +0.00163 | +0.0% | [-0.036; 0.0393] | 1 | não |
| filial1-filial2 | udp | 1024 | jitter_ms | 0.323 | 0.362 | +0.039 | +12.1% | [0.004; 0.074] | 1 | não |
| filial1-filial2 | udp | 1024 | perda_pct | 0.0342 | 0.114 | +0.0797 | +232.7% | [-0.0659; 0.225] | 1 | não |
| filial1-filial2 | udp | 1024 | vazao_mbps | 9 | 8.99 | -0.00713 | -0.1% | [-0.0202; 0.00591] | 1 | não |
| filial1-filial2 | udp | 1400 | jitter_ms | 0.396 | 0.415 | +0.0183 | +4.6% | [-0.025; 0.0616] | 1 | não |
| filial1-filial2 | udp | 1400 | perda_pct | 0.00243 | 0.0114 | +0.00897 | +368.5% | [-0.00364; 0.0216] | 1 | não |
| filial1-filial2 | udp | 1400 | vazao_mbps | 9 | 9 | -0.000733 | -0.0% | [-0.00188; 0.000409] | 1 | não |
| filial1-filial2 | udp | 512 | jitter_ms | 0.241 | 0.219 | -0.0218 | -9.1% | [-0.0676; 0.024] | 1 | não |
| filial1-filial2 | udp | 512 | perda_pct | 0.169 | 0.206 | +0.0376 | +22.3% | [-0.169; 0.244] | 1 | não |
| filial1-filial2 | udp | 512 | vazao_mbps | 8.98 | 8.98 | -0.00343 | -0.0% | [-0.022; 0.0151] | 1 | não |
| filial1-filial2 | udp | 64 | jitter_ms | 0.0916 | 0.112 | +0.0203 | +22.1% | [-0.00081; 0.0413] | 1 | não |
| filial1-filial2 | udp | 64 | perda_pct | 42.9 | 42.6 | -0.242 | -0.6% | [-0.633; 0.149] | 1 | não |
| filial1-filial2 | udp | 64 | vazao_mbps | 5.14 | 5.16 | +0.0218 | +0.4% | [-0.0134; 0.057] | 1 | não |
| matriz-filial1 | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| matriz-filial1 | latencia | — | rtt_medio_ms | 29.5 | 27.5 | -2.04 | -6.9% | [-3.01; -1.07] | 0.0216 | sim |
| matriz-filial1 | latencia | — | rtt_p95_ms | 32.5 | 30.2 | -2.29 | -7.0% | [-3.43; -1.14] | 0.0521 | não |
| matriz-filial1 | tcp | — | retrans | 5.17 | 13.1 | +7.97 | +154.2% | [-8.15; 24.1] | 1 | não |
| matriz-filial1 | tcp | — | vazao_mbps | 19 | 19 | -0.00597 | -0.0% | [-0.021; 0.00903] | 1 | não |
| matriz-filial1 | udp | 1024 | jitter_ms | 0.272 | 0.272 | +0.000533 | +0.2% | [-0.0383; 0.0393] | 1 | não |
| matriz-filial1 | udp | 1024 | perda_pct | 0.029 | 0.13 | +0.101 | +347.4% | [0.0335; 0.168] | 0.815 | não |
| matriz-filial1 | udp | 1024 | vazao_mbps | 18 | 18 | -0.0181 | -0.1% | [-0.03; -0.00613] | 0.766 | não |
| matriz-filial1 | udp | 1400 | jitter_ms | 0.335 | 0.302 | -0.0322 | -9.6% | [-0.147; 0.0823] | 1 | não |
| matriz-filial1 | udp | 1400 | perda_pct | 0.0191 | 0.257 | +0.238 | +1245.2% | [0.0227; 0.453] | 1 | não |
| matriz-filial1 | udp | 1400 | vazao_mbps | 18 | 18 | -0.0429 | -0.2% | [-0.0816; -0.00423] | 1 | não |
| matriz-filial1 | udp | 512 | jitter_ms | 0.312 | 0.343 | +0.031 | +10.0% | [-0.0081; 0.0702] | 1 | não |
| matriz-filial1 | udp | 512 | perda_pct | 2.95 | 7.94 | +4.99 | +169.1% | [4.03; 5.95] | 4.3e-11 | sim |
| matriz-filial1 | udp | 512 | vazao_mbps | 17.5 | 16.6 | -0.898 | -5.1% | [-1.07; -0.726] | 4.33e-11 | sim |
| matriz-filial1 | udp | 64 | jitter_ms | 0.0992 | 0.12 | +0.0207 | +20.9% | [-0.0617; 0.103] | 1 | não |
| matriz-filial1 | udp | 64 | perda_pct | 64.1 | 65.3 | +1.15 | +1.8% | [-0.232; 2.52] | 1 | não |
| matriz-filial1 | udp | 64 | vazao_mbps | 6.46 | 6.25 | -0.206 | -3.2% | [-0.454; 0.0417] | 1 | não |
| matriz-filial2 | latencia | — | perda_pct | 0 | 0 | +0 |  | [0; 0] | 1 | não |
| matriz-filial2 | latencia | — | rtt_medio_ms | 69.3 | 68 | -1.29 | -1.9% | [-2.23; -0.345] | 1 | não |
| matriz-filial2 | latencia | — | rtt_p95_ms | 71.9 | 70.9 | -1.03 | -1.4% | [-2; -0.0571] | 1 | não |
| matriz-filial2 | tcp | — | retrans | 1.83 | 0.7 | -1.13 | -61.8% | [-3.31; 1.04] | 1 | não |
| matriz-filial2 | tcp | — | vazao_mbps | 9.32 | 9.33 | +0.00383 | +0.0% | [-0.00717; 0.0148] | 1 | não |
| matriz-filial2 | udp | 1024 | jitter_ms | 0.249 | 0.246 | -0.00283 | -1.1% | [-0.0418; 0.0362] | 1 | não |
| matriz-filial2 | udp | 1024 | perda_pct | 0.00473 | 0.00413 | -0.0006 | -12.7% | [-0.012; 0.0108] | 1 | não |
| matriz-filial2 | udp | 1024 | vazao_mbps | 9 | 9 | +0.000367 | +0.0% | [-0.000716; 0.00145] | 1 | não |
| matriz-filial2 | udp | 1400 | jitter_ms | 0.285 | 0.28 | -0.00523 | -1.8% | [-0.0661; 0.0557] | 1 | não |
| matriz-filial2 | udp | 1400 | perda_pct | 0.0374 | 0.0382 | +0.000833 | +2.2% | [-0.0829; 0.0845] | 1 | não |
| matriz-filial2 | udp | 1400 | vazao_mbps | 9 | 9 | +0.0001 | +0.0% | [-0.00744; 0.00764] | 1 | não |
| matriz-filial2 | udp | 512 | jitter_ms | 0.192 | 0.171 | -0.021 | -10.9% | [-0.0868; 0.0448] | 1 | não |
| matriz-filial2 | udp | 512 | perda_pct | 0.127 | 0.22 | +0.0925 | +72.8% | [-0.0894; 0.274] | 1 | não |
| matriz-filial2 | udp | 512 | vazao_mbps | 8.99 | 8.98 | -0.00833 | -0.1% | [-0.0247; 0.00801] | 1 | não |
| matriz-filial2 | udp | 64 | jitter_ms | 0.116 | 0.139 | +0.0226 | +19.4% | [-0.00944; 0.0547] | 1 | não |
| matriz-filial2 | udp | 64 | perda_pct | 42.7 | 42.7 | +0.0046 | +0.0% | [-0.0497; 0.0589] | 1 | não |
| matriz-filial2 | udp | 64 | vazao_mbps | 5.16 | 5.16 | -0.0004 | -0.0% | [-0.00526; 0.00446] | 1 | não |