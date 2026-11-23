# Segurança — etapa A (TCC-etapa-A)

## Origem: HOST-INVADIDO

**Por equipamento (métrica principal):**

- Equipamentos alcançáveis: **16/16**; com serviço aberto: **13**
- Serviços expostos: **23** (de gerência em equipamentos de rede: **14**)
- Vulnerabilidades expostas (equipamento × CVE): **181** {'media': 80, 'alta': 46, 'baixa': 44, 'critica': 11}

**Por endereço (caminhos de exposição):**

- Endereços alcançáveis: **24/28** (16 equipamentos)
- Endereços com serviço aberto: **21**; serviços abertos: **35** {'servidor': 6, 'estacao': 0, 'firewall': 15, 'roteador': 6, 'switch': 8}
- Serviços de gerência expostos em equipamentos de rede: **24**
- Servidores alcançáveis com serviço: APLICACAO, ARQUIVOS
- Vulnerabilidades expostas (serviço × CVE): **255** {'media': 116, 'alta': 62, 'baixa': 60, 'critica': 17}; CVEs únicas: 72
- Serviços sem versão completa identificada (fora da contagem de CVEs): 26

## Origem: PC-FIL1

**Por equipamento (métrica principal):**

- Equipamentos alcançáveis: **16/16**; com serviço aberto: **13**
- Serviços expostos: **23** (de gerência em equipamentos de rede: **14**)
- Vulnerabilidades expostas (equipamento × CVE): **181** {'media': 80, 'alta': 46, 'baixa': 44, 'critica': 11}

**Por endereço (caminhos de exposição):**

- Endereços alcançáveis: **24/28** (16 equipamentos)
- Endereços com serviço aberto: **19**; serviços abertos: **33** {'servidor': 6, 'estacao': 0, 'firewall': 15, 'roteador': 6, 'switch': 6}
- Serviços de gerência expostos em equipamentos de rede: **22**
- Servidores alcançáveis com serviço: APLICACAO, ARQUIVOS
- Vulnerabilidades expostas (serviço × CVE): **255** {'media': 116, 'alta': 62, 'baixa': 60, 'critica': 17}; CVEs únicas: 72
- Serviços sem versão completa identificada (fora da contagem de CVEs): 24

## Produtos encontrados e CVEs conhecidas

| CPE | CVEs | críticas | altas | médias | baixas |
|---|---|---|---|---|---|
| cpe:/a:cisco:telnet | sem versão completa | 0 | 0 | 0 | 0 |
| cpe:/a:lighttpd:lighttpd:1.4.85 | 0 | 0 | 0 | 0 | 0 |
| cpe:/a:nlnetlabs:unbound:1.25.1 | 37 | 3 | 8 | 18 | 8 |
| cpe:/a:openbsd:openssh:9.7 | 35 | 1 | 11 | 13 | 10 |
| cpe:/a:samba:samba:4 | sem versão completa | 0 | 0 | 0 | 0 |
| cpe:/o:cisco:ios | sem versão completa | 0 | 0 | 0 | 0 |