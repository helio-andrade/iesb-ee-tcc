# Zero Trust em rede corporativa: scripts e dados

Scripts e dados do Trabalho de Conclusão de Curso (TCC) de Engenharia Elétrica do Centro Universitário IESB, 2026:

> **Zero Trust em rede corporativa: ganho de segurança versus impacto no desempenho**
> Hélio Andrade da Silva Júnior. Orientador: Prof. Odilon Francisco Pavón Duarte.

O trabalho mediu, em um laboratório emulado no GNS3, o ganho de segurança e o custo de desempenho de controles
Zero Trust em uma rede corporativa com matriz e duas filiais (equipamentos Cisco IOL e firewalls OPNsense 26.7),
implantada em quatro etapas na mesma topologia:

| Etapa | Modelo | Controles |
|---|---|---|
| 0 | Rede plana | Uma sub-rede por unidade; firewalls liberam todo o tráfego; gerência dos Cisco por Telnet |
| A | Perimetral | VLANs de usuários, servidores e gerência roteadas sem restrição pelo switch de núcleo; firewalls filtram só a WAN |
| B1 | Zero Trust | Servidores em enclave atrás do firewall da matriz; bloqueio padrão; portal cativo com RADIUS; ACLs; DAI e port security; gerência por SSH com AAA |
| B2 | Zero Trust com criptografia | B1 mais túneis IPsec (IKEv2) em estrela entre os firewalls |

Este repositório tem **os scripts** que montaram as etapas, executaram os ensaios e analisaram os resultados, e
**os dados** obtidos. Não inclui os projetos do GNS3 nem as imagens dos equipamentos.

## Estrutura

```
scripts/            scripts Python (a mesma versão que gerou os dados)
dados/ensaios/      desempenho: uma pasta por bateria, com os dados brutos de cada repetição
dados/seguranca/    segurança: varreduras do Nmap e vulnerabilidades, por etapa
dados/analise/      estatística: resumo de cada bateria, comparações entre etapas e conferência com o SciPy
```

## Reproduzir a análise estatística

Só a análise pode ser refeita sem o laboratório: ela parte dos dados brutos de `dados/ensaios`.

```
python scripts/analisar.py                       # resumo de cada bateria (média, desvio, p95, IC 95%)
python scripts/analisar.py --comparar 0 A        # teste de Welch com ajuste de Holm: etapa A em relação à 0
python scripts/conferir_scipy.py                 # refaz todos os testes com o SciPy e compara
```

As comparações publicadas em `dados/analise` são estas nove:

```
0-rodada1 x 0    0 x 0-verificacao    0 x A    0 x B1    0 x B2
A x B1           B1 x B2              B1 x B2-teste      B2-teste x B2
```

- O `analisar.py` usa só a biblioteca padrão do Python (3.14): t de Welch com graus de liberdade de
  Welch-Satterthwaite, p bicaudal pela função beta incompleta regularizada, ajuste de Holm e IC 95% pela t de Student.
- O `conferir_scipy.py` refaz os 3.204 testes com `scipy.stats.ttest_ind(equal_var=False)`. A decisão (significativa
  ou não, a 5%, após o ajuste de Holm) é a mesma em todos, e os valores p coincidem até cerca de 2 × 10⁻¹².
- Rodar os comandos acima nesta pasta gera de novo, com o mesmo conteúdo, os arquivos de `dados/analise`.

Instalação das bibliotecas (o SciPy só é necessário para a conferência; o paramiko, para o laboratório):

```
python -m pip install -r scripts/requirements.txt
```

Nos comentários dos scripts, os caminhos aparecem como `lab/scripts` e `lab/dados`, a estrutura original do
trabalho. Aqui eles são `scripts` e `dados`, e os scripts funcionam sem alteração, porque procuram `dados` na pasta
acima da sua.

## Dados

### Desempenho (`dados/ensaios`)

Em cada bateria, 30 repetições, após uma de aquecimento descartada, de cada teste em quatro caminhos: rede local da
matriz (`LAN-matriz`), matriz para filial 1 (20 Mbit/s, RTT de 20 ms), matriz para filial 2 (10 Mbit/s, 60 ms) e
filial 1 para filial 2.

| Pasta | O que é |
|---|---|
| `etapa-0`, `etapa-A`, `etapa-B1`, `etapa-B2` | baterias oficiais das quatro etapas |
| `etapa-0-rodada1` | primeira rodada da etapa 0, mantida para medir a variação entre rodadas |
| `etapa-0-verificacao` | 5 repetições da etapa 0 depois da troca dos servidores e da gerência por Telnet |
| `etapa-B2-teste` | rodada adicional completa da B2 (30 repetições, sem aquecimento), de reprodutibilidade |
| `etapa-B2-com-falha-SW-ACC1` | bateria da B2 em que o switch de acesso da matriz travou (falha do emulador no *port security*); as repetições afetadas foram refeitas na `etapa-B2` |

Arquivos de cada bateria:

| Arquivo | Conteúdo |
|---|---|
| `resultados.csv` | uma linha por repetição, caminho, teste e tamanho de pacote: vazão, retransmissões, jitter, perda, RTT médio, p95, mínimo e máximo |
| `cpu.csv` | CPU (% de um núcleo) e memória de cada equipamento durante cada teste |
| `ambiente.csv` | carga da GNS3 VM e do computador hospedeiro durante cada teste |
| `bruto.jsonl` | saída original do fping e JSON completo do iperf3 de cada teste |
| `meta.json` | caminhos, tamanhos de pacote, equipamentos e comandos usados |
| `portal.csv` | (B1 e B2) 30 autenticações no portal cativo: redirecionamento sem sessão, recusa da senha errada, tempo de login e do primeiro acesso |

Os comandos: latência com `fping -C 20 -p 100 -t 1000`; TCP com `iperf3 -t 10`; UDP com `iperf3 -u` por 5 s a 90% da
capacidade do caminho, com pacotes de 64, 512, 1024 e 1400 bytes; CPU pela variação de `utime + stime` dos processos
QEMU e IOL e pelo `cpuacct` dos contêineres. Os arquivos `.log` são o registro de execução de cada bateria.

### Segurança (`dados/seguranca`)

Por etapa, a partir de dois hosts considerados comprometidos (`HOST-INVADIDO`, na matriz, e `PC-FIL1`):

| Arquivo | Conteúdo |
|---|---|
| `*_descoberta.xml`, `*_servicos.xml` | saída XML do Nmap: descoberta sem ARP e varredura SYN com detecção de versão nas 1000 portas TCP mais comuns |
| `alcance.csv` | equipamentos alcançáveis a partir de cada origem |
| `servicos.csv` | serviços expostos, com produto, versão e CPE |
| `vulnerabilidades.csv` | CVEs associadas a cada CPE, com CVSS |
| `resumo.json`, `resumo.md` | contagens por etapa e origem |
| `vulners_cache.json` | respostas da API pública do vulners.com usadas na consulta das CVEs |

### Estatística (`dados/analise`)

- `etapa-*_desempenho.csv` e `etapa-*_cpu.csv`: n, média, desvio-padrão, p95 e meia largura do IC 95% de cada métrica.
- `comparacao_*.csv`: para cada uma das 356 métricas do par de etapas, a diferença, o IC 95% da diferença, t, graus
  de liberdade, p, p ajustado por Holm e a decisão a 5%.
- `conferencia_scipy.csv` e `.md`: resultado da conferência independente com o SciPy.
- Os `.md` trazem as mesmas tabelas em formato legível.

## Reproduzir o laboratório

Os scripts falam com o controlador do GNS3 (2.2.61) e com a GNS3 VM (endereço na variável `GNS3_VM_HOST`; padrão
`192.168.16.130`). Eles criam os equipamentos a partir de templates do GNS3 que **não estão neste repositório**:

| Template | Uso |
|---|---|
| `TCC - IOL L3 15.4` | roteadores (Cisco IOL; imagem proprietária, não distribuída) |
| `TCC - IOL L2 17.15` | switches (Cisco IOL L2; imagem proprietária, não distribuída) |
| `TCC - OPNsense 26.7` | firewalls |
| `TCC - Host` | computadores (contêiner Docker com fping, iperf3 e Nmap) |
| `TCC - Servidor` | servidores de aplicação e de arquivos (contêiner com OpenSSH, lighttpd e Samba) |
| `TCC - Provedor` | provedor da WAN, com atraso e limite de banda emulados |

Ordem de execução:

1. `montar_etapa0.py`, `servidores_etapa0.py` e `gerencia_telnet_etapa0.py`: etapa 0 (`TCC-etapa-0`).
2. Duplicar o projeto no GNS3 e rodar `montar_etapaA.py` (A), depois `montar_etapaB1.py` (B1) e `montar_etapaB2.py`
   (B2), cada um sobre a cópia da etapa anterior.
3. Em cada etapa: `ensaio.py --projeto TCC-etapa-X --etapa X --reps 30` (desempenho),
   `seguranca.py --projeto TCC-etapa-X --etapa X` (segurança) e, nas etapas B, `medir_portal.py` (autenticação).
4. `analisar.py` e `conferir_scipy.py` (estatística).

`gns3lab.py` reúne as funções comuns; `rotulos_etapas.py` e `rotulos_ip.py` só escrevem anotações no desenho do
GNS3, para as figuras.

**Senhas:** os scripts trazem as senhas do laboratório (equipamentos, portal, RADIUS). Elas valem apenas dentro da
rede emulada e isolada do GNS3 e foram mantidas para que os scripts sejam os mesmos que geraram os dados. As chaves
da API dos OPNsense e as chaves pré-compartilhadas do IPsec são geradas pelos próprios scripts em cada montagem e
não estão no repositório.

## Alterações em relação aos arquivos originais

- Nos arquivos `.log`, o caminho absoluto da pasta do trabalho no computador do autor foi removido; os caminhos ficaram
  relativos à raiz do repositório.
- `dados/analise` foi gerada de novo pelos scripts desta pasta. O conteúdo é o mesmo da análise original, com o
  resumo da bateria `etapa-B2-com-falha-SW-ACC1` a mais.

## Licença

Código (`scripts/`): licença MIT (arquivo `LICENSE`). Dados (`dados/`):
[Creative Commons Atribuição 4.0 Internacional (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/deed.pt-br).

## Como citar

Veja `CITATION.cff`, ou cite o artigo e este repositório:

> H. A. da Silva Júnior, *Zero Trust em rede corporativa: scripts e dados*, versão 1.0, 2026. [Online].
> Disponível: https://github.com/helio-andrade/iesb-ee-tcc
