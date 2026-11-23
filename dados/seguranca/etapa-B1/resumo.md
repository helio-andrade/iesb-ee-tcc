# Segurança — etapa B1 (TCC-etapa-B1)

## Origem: HOST-INVADIDO

**Por equipamento (métrica principal):**

- Equipamentos alcançáveis: **3/16**; com serviço aberto: **1**
- Serviços expostos: **2** (de gerência em equipamentos de rede: **0**)
- Vulnerabilidades expostas (equipamento × CVE): **37** {'media': 18, 'alta': 8, 'baixa': 8, 'critica': 3}

**Por endereço (caminhos de exposição):**

- Endereços alcançáveis: **7/28** (3 equipamentos)
- Endereços com serviço aberto: **4**; serviços abertos: **5** {'servidor': 0, 'estacao': 0, 'firewall': 5, 'roteador': 0, 'switch': 0}
- Serviços de gerência expostos em equipamentos de rede: **0**
- Servidores alcançáveis com serviço: nenhum
- Vulnerabilidades expostas (serviço × CVE): **148** {'media': 72, 'alta': 32, 'baixa': 32, 'critica': 12}; CVEs únicas: 37
- Serviços sem versão completa identificada (fora da contagem de CVEs): 1

## Origem: PC-FIL1

**Por equipamento (métrica principal):**

- Equipamentos alcançáveis: **2/16**; com serviço aberto: **0**
- Serviços expostos: **0** (de gerência em equipamentos de rede: **0**)
- Vulnerabilidades expostas (equipamento × CVE): **0** {}

**Por endereço (caminhos de exposição):**

- Endereços alcançáveis: **2/28** (2 equipamentos)
- Endereços com serviço aberto: **0**; serviços abertos: **0** {'servidor': 0, 'estacao': 0, 'firewall': 0, 'roteador': 0, 'switch': 0}
- Serviços de gerência expostos em equipamentos de rede: **0**
- Servidores alcançáveis com serviço: nenhum
- Vulnerabilidades expostas (serviço × CVE): **0** {}; CVEs únicas: 0
- Serviços sem versão completa identificada (fora da contagem de CVEs): 0

## Produtos encontrados e CVEs conhecidas

| CPE | CVEs | críticas | altas | médias | baixas |
|---|---|---|---|---|---|
| cpe:/a:nlnetlabs:unbound:1.25.1 | 37 | 3 | 8 | 18 | 8 |