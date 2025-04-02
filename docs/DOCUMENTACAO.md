# Documentação do Sistema de Coleta de Dados Climáticos

## Visão Geral

O Sistema de Coleta de Dados Climáticos é uma solução desenvolvida para automatizar a obtenção, armazenamento e análise de dados meteorológicos de múltiplas fontes. O sistema utiliza a API OpenWeather como fonte principal e a API do INMET (Instituto Nacional de Meteorologia do Brasil) como backup, garantindo resiliência e continuidade na coleta de dados.

Esta documentação fornece instruções detalhadas sobre instalação, configuração, uso e manutenção do sistema para usuários e administradores.

## Índice

1. [Objetivo e Funcionalidades](#objetivo-e-funcionalidades)
2. [Requisitos do Sistema](#requisitos-do-sistema)
3. [Instalação](#instalação)
4. [Estrutura do Sistema](#estrutura-do-sistema)
5. [Interface de Linha de Comando](#interface-de-linha-de-comando)
6. [Configuração](#configuração)
7. [Uso do Sistema](#uso-do-sistema)
8. [Análise de Dados](#análise-de-dados)
9. [Automação de Coleta](#automação-de-coleta)
10. [Solução de Problemas](#solução-de-problemas)
11. [FAQ](#faq)

## Objetivo e Funcionalidades

### Objetivo

Fornecer uma plataforma robusta para coleta automática de dados climáticos de múltiplas regiões agrícolas brasileiras, para apoiar modelos preditivos de demanda de insumos agrícolas que consideram variáveis climáticas como fatores de influência.

### Principais Funcionalidades

- **Coleta de Dados Atuais**: Obtenção de dados meteorológicos dos últimos 7 dias, com atualizações diárias.
- **Coleta de Dados Históricos**: Acesso a até 15 anos de dados climáticos históricos para análises de longo prazo.
- **Sistema de Failover Automático**: Transição automática para a API secundária (INMET) caso a principal (OpenWeather) falhe.
- **Validação de Dados**: Verificação de consistência e integridade dos dados coletados.
- **Prevenção de Duplicação**: Mecanismos para evitar armazenamento duplicado de informações.
- **Estrutura Organizacional**: Dados armazenados em formato estruturado, organizados por fonte, região, ano e mês.
- **Interface de Linha de Comando**: CLI completo para interação com todas as funcionalidades do sistema.
- **Ferramentas de Análise**: Scripts para visualização e análise estatística dos dados coletados.
- **Gestão de Regiões**: Configuração externa e flexível de regiões monitoradas.

## Requisitos do Sistema

### Hardware Recomendado

- Processador: 2 GHz dual-core ou superior
- Memória RAM: 4GB ou superior (8GB recomendado para processamento de grandes volumes históricos)
- Espaço em Disco: Mínimo de 5GB livres para instalação e dados (mais espaço pode ser necessário dependendo da quantidade de regiões e período histórico)
- Conexão à Internet: Estável, mínimo 1 Mbps

### Software Necessário

- Python 3.7 ou superior
- Sistema operacional: Windows 10/11, macOS 10.14+, ou Linux (Ubuntu 18.04+, Debian 10+, CentOS 7+)
- Gerenciador de pacotes pip

### Dependências Python

Todas as dependências estão listadas no arquivo `requisitos.txt`:

- requests: Para requisições HTTP às APIs
- pandas: Para manipulação e análise de dados
- matplotlib: Para geração de gráficos
- numpy: Para operações numéricas
- seaborn: Para visualizações estatísticas avançadas
- colorama: Para interface colorida no terminal
- tabulate: Para formatação de tabelas no terminal
- inmetpy (opcional): Para acesso à API do INMET

## Instalação

### Instalação Manual

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seuusuario/sistema_dados_climaticos.git
   cd sistema_dados_climaticos
   ```

2. **Instale as dependências**:
   ```bash
   pip install -r requisitos.txt
   ```

3. **Verifique a instalação**:
   ```bash
   python cli.py
   ```

### Instalação Automatizada

Execute o script de instalação que configura o ambiente completo:

```bash
chmod +x instalar.sh
./instalar.sh
```

O script realizará as seguintes tarefas:
- Verificar requisitos do sistema
- Criar um ambiente virtual Python
- Instalar todas as dependências
- Configurar diretórios de dados e logs
- Guiar na configuração de chaves de API
- Oferecer configuração opcional de execução automatizada

## Estrutura do Sistema

### Estrutura de Diretórios

```
sistema_dados_climaticos/
├── cli.py                  # Interface de linha de comando
├── src/                    # Código-fonte
│   ├── coletor_climatico.py
│   ├── analisador_dados.py
│   ├── exemplo_analise.py
│   └── executar_coleta.py
├── config/                 # Arquivos de configuração
│   ├── regioes.json
│   └── credenciais.json
├── dados/                  # Dados coletados
│   ├── openweather/
│   │   └── AAAA/MM/        # Organizados por ano/mês
│   └── inmet/
│       └── AAAA/MM/        # Organizados por ano/mês 
├── logs/                   # Logs de execução
│   └── AAAA/MM/            # Organizados por ano/mês
├── docs/                   # Documentação
│   └── DOCUMENTACAO.md
├── temp/                   # Arquivos temporários
├── requisitos.txt          # Dependências
├── README.md               # Documentação resumida
└── instalar.sh             # Script de instalação
```

### Componentes Principais

- **cli.py**: Interface de linha de comando interativa
- **coletor_climatico.py**: Núcleo do sistema com a lógica de coleta
- **analisador_dados.py**: Funções para análise básica dos dados
- **exemplo_analise.py**: Interface interativa para análises avançadas

### Organização de Dados e Logs

Tanto os dados coletados quanto os logs são organizados em uma estrutura hierárquica:

1. **Dados**:
   ```
   dados/
   ├── openweather/         # Fonte primária
   │   └── 2025/            # Ano
   │       └── 04/          # Mês (04 = abril)
   │           ├── atual_Ribeirao_Preto_SP_20250402.csv
   │           └── historico_Sao_Paulo_SP_20250402.csv
   ├── inmet/               # Fonte secundária (backup)
       └── 2025/            # Ano
           └── 04/          # Mês
               └── ...
   ```

2. **Logs**:
   ```
   logs/
   └── 2025/                # Ano
       └── 04/              # Mês
           ├── coletor_20250402.log
           ├── execucao_20250402_123045.log
           └── cli_20250402.log
   ```

Esta estrutura facilita:
- Organização cronológica dos dados
- Rotação e limpeza de logs antigos
- Backup seletivo de períodos específicos

## Interface de Linha de Comando

### Modos de Operação

O CLI oferece dois modos de operação:

#### 1. Modo Interativo

Inicie o modo interativo sem argumentos:
```bash
python cli.py
```

Este modo apresenta um menu completo com todas as funcionalidades do sistema, facilitando a navegação e uso.

#### 2. Modo de Comando

Para automação ou uso em scripts:
```bash
# Coleta de dados atuais
python cli.py coleta --modo atual

# Coleta de dados históricos
python cli.py coleta --modo historico

# Coleta para regiões específicas
python cli.py coleta --regioes Ribeirao_Preto_SP Brasilia_DF

# Iniciar análise interativa
python cli.py analise

# Mostrar ajuda
python cli.py ajuda
```

### Funcionalidades do CLI

O CLI organiza as funcionalidades em menus para fácil acesso:

1. **Coleta de Dados**
   - Coletar dados atuais (últimos 7 dias)
   - Coletar dados históricos
   - Coletar todos os dados (atual + histórico)
   - Coletar dados para região específica

2. **Consulta e Análise**
   - Listar regiões com dados disponíveis
   - Visualizar dados de uma região
   - Visualizar dados históricos
   - Análise avançada (interface interativa)
   - Comparar regiões

3. **Gerenciar Regiões**
   - Listar regiões configuradas
   - Adicionar nova região
   - Remover região
   - Importar regiões de CSV
   - Exportar regiões para CSV

4. **Exportação de Dados**
   - Exportar dados para CSV
   - Exportar dados para Excel
   - Exportar gráficos

5. **Logs e Monitoramento**
   - Visualizar logs do sistema
   - Verificar estatísticas de coleta
   - Limpar logs antigos

6. **Configurações**
   - Configurar credenciais de API
   - Configurar frequência de coleta
   - Verificar diretórios do sistema

7. **Ajuda e Documentação**
   - Visualização da documentação completa

## Configuração

### Credenciais de API

O sistema armazena as credenciais das APIs no arquivo `config/credenciais.json`:

```json
{
  "openweather": {
    "api_key": "sua_api_key_aqui"
  },
  "inmet": {
    "token": "seu_token_aqui"
  }
}
```

Você pode configurar as credenciais das seguintes formas:

1. **Através do CLI**:
   - Execute o CLI em modo interativo
   - Selecione "Configurações" > "Configurar credenciais de API"
   - Siga as instruções na tela

2. **Editando o arquivo diretamente**:
   - Abra o arquivo `config/credenciais.json` em um editor de texto
   - Atualize os valores de `api_key` e `token`
   - Salve o arquivo

### Configuração de Regiões

As regiões monitoradas são definidas no arquivo `config/regioes.json`:

```json
{
  "regioes_agricolas": [
    {
      "nome": "Ribeirao_Preto_SP",
      "descricao": "Região de Ribeirão Preto - SP (Cana-de-açúcar)",
      "latitude": -21.17,
      "longitude": -47.81,
      "estacao_inmet": "A711"
    },
    {
      "nome": "Brasilia_DF",
      "descricao": "Região de Brasília - DF (Soja e Milho)",
      "latitude": -15.78,
      "longitude": -47.93,
      "estacao_inmet": "A001"
    }
  ]
}
```

### Gerenciamento de Regiões pelo CLI

O CLI oferece várias opções para gerenciar regiões:

1. **Adicionar Nova Região**:
   - No menu principal, selecione "Gerenciar Regiões" > "Adicionar nova região"
   - Forneça os dados solicitados: nome, descrição, coordenadas, código da estação INMET

2. **Importar de CSV**:
   Para importação em lote, crie um arquivo CSV com as colunas:
   - nome: Identificador único sem espaços
   - descricao: Descrição legível da região
   - latitude: Valor decimal (ex: -21.17)
   - longitude: Valor decimal (ex: -47.81)
   - estacao_inmet: Código da estação INMET mais próxima

   No CLI, selecione "Gerenciar Regiões" > "Importar regiões de CSV" e forneça o caminho do arquivo.

### Encontrando Códigos de Estações INMET

Para encontrar o código da estação INMET mais próxima:
1. Acesse o [mapa de estações do INMET](https://mapas.inmet.gov.br/)
2. Localize a estação automática mais próxima da região desejada
3. Anote o código da estação (formato: A000)

## Uso do Sistema

### Coleta de Dados

#### Coleta de Dados Atuais

Para coletar dados meteorológicos dos últimos 7 dias:

**Via CLI Interativo**:
1. Execute `python cli.py`
2. Selecione "Coleta de Dados" > "Coletar dados atuais"

**Via Linha de Comando**:
```bash
python cli.py coleta --modo atual
```

Opções adicionais:
- `--regioes NOME1 NOME2` - Para coletar apenas regiões específicas
- `--dias 10` - Ajustar o número de dias para coleta (1-30)

#### Coleta de Dados Históricos

Para coletar dados históricos (até 15 anos atrás):

**Via CLI Interativo**:
1. Execute `python cli.py`
2. Selecione "Coleta de Dados" > "Coletar dados históricos"

**Via Linha de Comando**:
```bash
python cli.py coleta --modo historico
```

Opções adicionais:
- `--regioes NOME1 NOME2` - Para coletar apenas regiões específicas
- `--anos 5` - Ajustar o número de anos de dados históricos (1-30)

#### Coleta para Região Específica

**Via CLI Interativo**:
1. Execute `python cli.py`
2. Selecione "Coleta de Dados" > "Coletar dados para região específica"
3. Selecione a região desejada da lista apresentada

**Via Linha de Comando**:
```bash
python cli.py coleta --regioes Ribeirao_Preto_SP --modo atual
```

### Visualização de Logs

Os logs são organizados por ano e mês, seguindo uma estrutura hierárquica semelhante aos dados coletados:

```
logs/
└── 2025/                # Ano
    └── 04/              # Mês (04 = abril)
        ├── coletor_20250402.log
        ├── execucao_20250402_123045.log
        └── cli_20250402.log
```

Esta organização facilita:
- Localização de logs específicos por período
- Manutenção e limpeza de logs antigos
- Análise de problemas históricos

**Via CLI Interativo**:
1. Execute `python cli.py`
2. Selecione "Logs e Monitoramento" > "Visualizar logs do sistema"
3. Selecione o arquivo de log que deseja visualizar

Também é possível acessar diretamente os arquivos de log navegando pela estrutura de diretórios:
```
logs/AAAA/MM/nome_do_log.log
```

Tipos de logs gerados pelo sistema:
- `coletor_AAAAMMDD.log`: Logs do processo de coleta de dados
- `execucao_AAAAMMDD_HHMMSS.log`: Logs de execução de coletas agendadas
- `cli_AAAAMMDD.log`: Logs da interface de linha de comando

### Limpeza de Logs Antigos

Para manter o sistema organizado, o CLI oferece opções para limpeza de logs:

1. Execute `python cli.py`
2. Selecione "Logs e Monitoramento" > "Limpar logs antigos"
3. Escolha uma das opções:
   - Manter apenas os logs dos últimos 7 dias
   - Manter apenas os logs do último mês
   - Manter apenas os 10 logs mais recentes
   - Limpar todos os logs

## Análise de Dados

### Analisador por Linha de Comando

Para análises básicas e visualizações rápidas:

**Via CLI Interativo**:
1. Execute `python cli.py`
2. Selecione "Consulta e Análise" > "Visualizar dados de uma região"
3. Selecione a região desejada

**Via Linha de Comando**:
```bash
# Listar regiões disponíveis
python src/analisador_dados.py --listar-regioes

# Visualizar temperatura de uma região
python src/analisador_dados.py --regiao Ribeirao_Preto_SP --grafico temp

# Visualizar todos os gráficos
python src/analisador_dados.py --regiao Brasilia_DF --grafico todos
```

### Analisador Interativo

Para análises mais detalhadas e exploratórias:

**Via CLI Interativo**:
1. Execute `python cli.py`
2. Selecione "Consulta e Análise" > "Análise avançada (interface interativa)"

**Via Linha de Comando**:
```bash
python cli.py analise
# ou diretamente:
python src/exemplo_analise.py
```

O analisador interativo oferece:
- Seleção de região por menu
- Escolha entre dados atuais ou históricos
- Múltiplas visualizações (temperatura, precipitação, correlações)
- Visualização de dados brutos
- Estatísticas descritivas
- Exportação de gráficos

### Exportação de Dados

O sistema permite exportar dados em diferentes formatos:

**Via CLI Interativo**:
1. Execute `python cli.py`
2. Selecione "Exportação de Dados"
3. Escolha o formato desejado:
   - CSV
   - Excel (requer instalação de openpyxl)
   - Gráficos (PNG)

Durante a exportação, você poderá selecionar:
- A região desejada
- O período de dados (última semana, mês, 3 meses, ano)
- O diretório de destino

## Automação de Coleta

### Usando Cron (Linux/Unix/Mac)

Para configurar execução diária automática:

1. Abra o editor crontab:
```bash
crontab -e
```

2. Adicione a linha para execução (exemplo: todos os dias às 02:00):
```
0 2 * * * cd /caminho/completo/para/sistema_dados_climaticos && python cli.py coleta --modo atual > /dev/null 2>&1
```

3. Para execução semanal de dados históricos (exemplo: todo domingo às 03:00):
```
0 3 * * 0 cd /caminho/completo/para/sistema_dados_climaticos && python cli.py coleta --modo historico > /dev/null 2>&1
```

### Usando Agendador de Tarefas (Windows)

1. Crie um arquivo batch (`coletar_diario.bat`):
```
@echo off
cd C:\caminho\para\sistema_dados_climaticos
python cli.py coleta --modo atual
```

2. Abra o Agendador de Tarefas do Windows:
   - Crie uma nova tarefa básica
   - Defina o gatilho como diário às 02:00
   - Como ação, selecione "Iniciar um programa"
   - Navegue até o arquivo batch criado

## Solução de Problemas

### Problemas Comuns e Soluções

| Problema | Causa Provável | Solução |
|----------|---------------|---------|
| Falha na API OpenWeather | Chave de API inválida ou limites excedidos | Verifique a chave API em config/credenciais.json; considere obter uma chave com mais requisições permitidas |
| Falha na API INMET | Token inválido ou estação inexistente | Verifique o token e o código da estação; consulte o portal do INMET para códigos atualizados |
| Falta de espaço em disco | Muitos dados históricos coletados | Use o CLI para limpar logs antigos; considere arquivar dados antigos |
| Erros de dependências | Bibliotecas Python desatualizadas ou faltando | Execute `pip install --upgrade -r requisitos.txt` |
| Permissões de arquivo | Problemas de acesso aos diretórios | Verifique permissões em "Configurações" > "Verificar diretórios do sistema" |

### Verificação de Diretórios

Para verificar e corrigir problemas de diretórios:

1. Execute `python cli.py`
2. Selecione "Configurações" > "Verificar diretórios do sistema"
3. O sistema verificará a existência e permissões de todos os diretórios
4. Se encontrar diretórios ausentes, oferecerá a opção de criá-los

### Verificação de Credenciais

Para verificar e atualizar credenciais:

1. Execute `python cli.py`
2. Selecione "Configurações" > "Configurar credenciais de API"
3. O sistema mostrará as credenciais atuais e permitirá atualizá-las

## FAQ

### Perguntas Frequentes

**P: Quantas regiões posso monitorar simultaneamente?**  
R: O sistema não tem limite técnico, mas recomendamos até 50 regiões para manter desempenho adequado e não exceder limites das APIs. Lembre-se que a API gratuita do OpenWeather tem limites de requisições por minuto.

**P: Como adicionar uma nova região agrícola?**  
R: Use o CLI em "Gerenciar Regiões" > "Adicionar nova região", ou edite diretamente o arquivo `config/regioes.json`.

**P: O sistema funciona offline?**  
R: Não. O sistema requer conexão internet para acessar as APIs de dados climáticos. Uma vez coletados, os dados podem ser analisados offline.

**P: Como aumentar o período histórico para mais de 15 anos?**  
R: Edite a constante `ANOS_HISTORICO` no arquivo `src/coletor_climatico.py`. Note que períodos muito longos aumentam significativamente o tempo de coleta e o armazenamento necessário.

**P: É possível exportar os dados para outras ferramentas?**  
R: Sim, os dados são armazenados em arquivos CSV que podem ser facilmente importados por Excel, Power BI, Tableau, R, e outras ferramentas de análise. Use a função "Exportação de Dados" no CLI.

**P: Ocorreu um erro de "chave API inválida" mesmo com a chave correta**  
R: Verifique se a chave foi ativada (pode levar algumas horas após o cadastro); tente usar a chave em um teste direto via navegador para confirmar sua validade.

**P: Como automatizar a coleta para execução diária?**  
R: Use cron (Linux/Mac) ou o Agendador de Tarefas (Windows) conforme detalhado na seção [Automação de Coleta](#automação-de-coleta).

**P: Os logs estão ocupando muito espaço. Como limpar logs antigos?**  
R: Use a função "Limpar logs antigos" no menu "Logs e Monitoramento" do CLI. Você pode escolher manter apenas logs recentes.

---

## Informações de Contato

Para suporte e esclarecimentos sobre o sistema, entre em contato:

- **Suporte Técnico**: suporte@exemplo.com.br
- **Repositório**: github.com/seuusuario/sistema_dados_climaticos
- **Documentação Online**: docs.exemplo.com/sistema_climatico

## Histórico de Atualizações

- **v1.0.0** (Abril/2025): Versão inicial
  - Implementação de coleta de dados atual e histórico
  - Sistema de failover entre APIs
  - CLI interativo completo
  - Organização de logs e dados por ano/mês