# Manual do Usuário - Sistema de Dados Climáticos

![Versão](https://img.shields.io/badge/versão-1.0.0-green)

## Índice

1. [Introdução](#introdução)
2. [Primeiros Passos](#primeiros-passos)
   - [Instalação](#instalação)
   - [Configuração Inicial](#configuração-inicial)
   - [Verificação do Sistema](#verificação-do-sistema)
3. [Usando o Sistema](#usando-o-sistema)
   - [Interface Principal](#interface-principal)
   - [Menu de Coleta de Dados](#menu-de-coleta-de-dados)
   - [Menu de Consulta e Análise](#menu-de-consulta-e-análise)
   - [Menu de Gerenciamento de Regiões](#menu-de-gerenciamento-de-regiões)
   - [Menu de Exportação](#menu-de-exportação)
   - [Menu de Logs](#menu-de-logs)
   - [Menu de Configurações](#menu-de-configurações)
4. [Uso em Linha de Comando](#uso-em-linha-de-comando)
5. [Automação de Coleta](#automação-de-coleta)
6. [Perguntas Frequentes](#perguntas-frequentes)
7. [Solução de Problemas](#solução-de-problemas)
8. [Suporte e Contato](#suporte-e-contato)

## Introdução

O Sistema de Dados Climáticos é uma ferramenta para coleta, armazenamento e análise de dados meteorológicos de múltiplas fontes. Foi desenvolvido especialmente para suportar modelos preditivos de demanda agrícola, fornecendo dados confiáveis sobre temperatura, precipitação, umidade e outras variáveis climáticas.

### Para quem é este sistema?

- **Analistas Agrícolas**: Para análise de impacto climático em safras
- **Pesquisadores**: Para estudos de correlação entre clima e produtividade
- **Gestores Agrícolas**: Para planejamento baseado em dados meteorológicos
- **Desenvolvedores de Modelos Preditivos**: Para obtenção organizada de dados históricos

### Principais recursos

- Coleta automática de dados de múltiplas fontes (OpenWeather e INMET)
- Sistema de failover para garantir a continuidade dos dados
- Organização dos dados por região, data e fonte
- Visualizações gráficas e análises estatísticas
- Exportação em formatos compatíveis com ferramentas de análise
- Interface amigável por linha de comando (CLI)

## Primeiros Passos

### Instalação

#### Instalação Automática (Recomendada)

1. Certifique-se de que seu sistema atende aos requisitos:
   - Python 3.7 ou superior
   - pip (gerenciador de pacotes Python)
   - 5GB de espaço em disco para armazenar dados históricos
   - Conexão à internet

2. Execute o script de instalação automatizada:
   ```bash
   chmod +x instalar.sh
   ./instalar.sh
   ```

   O script realizará:
   - Verificação de requisitos
   - Instalação de dependências
   - Criação de diretórios necessários
   - Configuração básica do ambiente

#### Instalação Manual

1. Instale as dependências Python:
   ```bash
   pip install -r requisitos.txt
   ```

2. Crie os diretórios necessários (caso não existam):
   ```bash
   mkdir -p dados/openweather dados/inmet logs config temp
   ```

3. Verifique a instalação:
   ```bash
   python cli.py
   ```

### Configuração Inicial

Após a instalação, você precisará configurar:

#### 1. Credenciais de API

Para configurar as chaves de API necessárias:

1. Execute o CLI e acesse o menu de configurações:
   ```bash
   python cli.py
   ```
   
2. Selecione: **Configurações** > **Configurar credenciais de API**

3. Insira sua chave API do OpenWeather (obrigatória) e token do INMET (opcional)

**Onde obter as chaves:**
- **OpenWeather**: Crie uma conta em [openweathermap.org](https://openweathermap.org/api) e obtenha uma chave gratuita
- **INMET**: Solicite acesso no site do [Instituto Nacional de Meteorologia](https://portal.inmet.gov.br/)

#### 2. Regiões de Interesse

O sistema permite gerenciar regiões para coleta de dados. Você pode:

1. Usar as regiões padrão já configuradas
2. Adicionar novas regiões através do menu:
   - Selecione: **Gerenciar Regiões** > **Adicionar nova região**
   - Informe nome, coordenadas e código da estação INMET mais próxima
3. Importar regiões de um arquivo CSV:
   - Prepare um CSV com colunas: `nome,descricao,latitude,longitude,estacao_inmet`
   - Selecione: **Gerenciar Regiões** > **Importar regiões de CSV**

### Verificação do Sistema

Após a instalação e configuração, é recomendado verificar se o sistema está funcionando corretamente:

1. Verifique os diretórios:
   - No CLI, selecione: **Configurações** > **Verificar diretórios do sistema**
   
2. Teste a coleta de dados com uma região:
   - Selecione: **Coleta de Dados** > **Coletar dados atuais**
   
3. Verifique se os dados foram coletados:
   - Selecione: **Consulta e Análise** > **Listar regiões com dados disponíveis**

## Usando o Sistema

### Interface Principal

O sistema apresenta uma interface interativa baseada em menus. Para iniciá-la, execute:

```bash
python cli.py
```

Você verá o menu principal com as seguintes opções:

1. **Coleta de Dados**: Coletar dados atuais ou históricos
2. **Consulta e Análise**: Visualizar e analisar dados coletados
3. **Gerenciar Regiões**: Configurar regiões para coleta
4. **Exportação de Dados**: Exportar dados em diversos formatos
5. **Logs e Monitoramento**: Visualizar logs do sistema
6. **Configurações**: Configurar APIs e verificar diretórios
7. **Ajuda e Documentação**: Acessar documentação interativa
0. **Sair**: Encerrar o programa

Navegue pelos menus digitando o número da opção desejada.

### Menu de Coleta de Dados

Neste menu, você pode coletar dados climáticos das regiões configuradas:

1. **Coletar dados atuais**: Coleta dados dos últimos 7 dias
   - Útil para análises de curto prazo e decisões imediatas
   - Execução mais rápida (geralmente menos de 5 minutos)
   
2. **Coletar dados históricos**: Coleta dados de até 15 anos atrás
   - Útil para análises de tendências e modelos preditivos
   - Pode levar mais tempo (até 30 minutos dependendo do número de regiões)
   
3. **Coletar todos os dados**: Combina as duas opções anteriores
   
4. **Coletar dados para região específica**: Permite selecionar uma região específica
   - Útil para atualizar apenas os dados de uma região de interesse
   - Opção mais rápida quando você não precisa atualizar todas as regiões

**Dicas de uso:**
- A coleta atual é recomendada para execução diária
- A coleta histórica pode ser executada semanalmente ou mensalmente
- O sistema evita duplicação de dados, então é seguro executar coletas repetidamente

### Menu de Consulta e Análise

Este menu permite visualizar e analisar os dados coletados:

1. **Listar regiões com dados disponíveis**: Mostra todas as regiões que possuem dados
   
2. **Visualizar dados de uma região**: Mostra estatísticas e gráficos para uma região específica
   - Exibe temperaturas médias, mínimas e máximas
   - Mostra estatísticas de umidade e precipitação
   - Permite gerar gráficos interativos
   
3. **Visualizar dados históricos**: Similar à opção anterior, mas focada em dados históricos
   
4. **Análise avançada**: Abre uma interface interativa com opções avançadas de análise
   - Correlações entre variáveis climáticas
   - Visualizações personalizáveis
   - Acesso a dados brutos
   
5. **Comparar regiões**: Permite comparar dados climáticos de duas regiões diferentes
   - Útil para análises comparativas
   - Exibe gráficos sobrepostos para fácil visualização

**Exemplos de análises úteis:**
- Compare a precipitação entre diferentes regiões produtoras
- Verifique padrões de temperatura nos últimos meses
- Correlacione umidade e precipitação para identificar padrões

### Menu de Gerenciamento de Regiões

Este menu permite configurar as regiões que serão monitoradas:

1. **Listar regiões configuradas**: Mostra todas as regiões atualmente configuradas
   
2. **Adicionar nova região**: Permite adicionar uma nova região para monitoramento
   - Você precisará fornecer:
     - Nome da região (sem espaços, ex: Sao_Paulo_SP)
     - Descrição (ex: Região de São Paulo - SP)
     - Latitude e longitude
     - Código da estação INMET mais próxima (opcional)
   
3. **Remover região**: Remove uma região da configuração
   
4. **Importar regiões de CSV**: Importa múltiplas regiões de um arquivo CSV
   - O formato do CSV deve ter as colunas: nome, descricao, latitude, longitude, estacao_inmet
   
5. **Exportar regiões para CSV**: Exporta as regiões configuradas para um arquivo CSV

**Como encontrar coordenadas geográficas:**
- Use o Google Maps: clique com o botão direito no local desejado e selecione "O que há aqui?"
- Use sites como [latlong.net](https://www.latlong.net/) para converter endereços em coordenadas

**Como encontrar o código da estação INMET:**
1. Acesse o [mapa de estações do INMET](https://mapas.inmet.gov.br/)
2. Localize a estação automática mais próxima da região desejada
3. Anote o código da estação (formato: A000)

### Menu de Exportação

Este menu permite exportar os dados coletados em diferentes formatos:

1. **Exportar dados para CSV**: Exporta dados em formato CSV (compatível com Excel e outras ferramentas)
   - Permite selecionar a região e o período desejado
   - Formata os dados para fácil análise
   
2. **Exportar dados para Excel**: Exporta diretamente para formato Excel (.xlsx)
   - Requer a biblioteca opcional openpyxl (incluída nos requisitos)
   
3. **Exportar gráficos**: Salva gráficos de temperatura, umidade e precipitação como imagens PNG
   - Útil para relatórios e apresentações
   - Alta qualidade para impressão

**Opções de período para exportação:**
- Última semana
- Último mês
- Últimos 3 meses
- Último ano
- Últimos 5 anos
- Todos os dados disponíveis

Por padrão, os arquivos são salvos na pasta Downloads do usuário.

### Menu de Logs

Este menu permite gerenciar os logs do sistema:

1. **Visualizar logs do sistema**: Permite visualizar os registros de atividade
   - Logs são organizados por data e tipo
   - Cores diferentes identificam erros, avisos e informações
   
2. **Verificar estatísticas de coleta**: Mostra estatísticas sobre os dados coletados
   - Quantidade de registros por região
   - Distribuição de dados por fonte
   
3. **Limpar logs antigos**: Remove logs antigos para economizar espaço
   - Opções para manter apenas logs recentes
   - Ajuda a manter o sistema organizado

Os logs são essenciais para diagnosticar problemas. Se encontrar algum erro, verifique os logs para mais detalhes.

### Menu de Configurações

Este menu permite ajustar as configurações do sistema:

1. **Configurar credenciais de API**: Gerencia as chaves de API para OpenWeather e INMET
   
2. **Configurar frequência de coleta**: Exibe informações sobre como automatizar a coleta
   
3. **Verificar diretórios do sistema**: Verifica se todos os diretórios necessários existem e têm permissões corretas

## Uso em Linha de Comando

Além do modo interativo, o sistema pode ser usado diretamente na linha de comando, o que é útil para automação e scripts.

### Comandos Principais

```bash
# Coleta de dados atuais para todas as regiões
python cli.py coleta --modo atual

# Coleta de dados históricos para todas as regiões
python cli.py coleta --modo historico

# Coleta para regiões específicas
python cli.py coleta --regioes Ribeirao_Preto_SP Brasilia_DF

# Coleta com período personalizado
python cli.py coleta --modo atual --dias 10

# Iniciar análise interativa
python cli.py analise

# Mostrar ajuda do sistema
python cli.py ajuda
```

### Exemplos de Uso Avançado

```bash
# Coletar dados atuais para uma região específica, limitando a 3 dias
python cli.py coleta --modo atual --regioes Petrolina_PE --dias 3

# Coletar dados históricos para duas regiões, limitando a 5 anos
python cli.py coleta --modo historico --regioes Ribeirao_Preto_SP Sorriso_MT --anos 5

# Executar silenciosamente (sem saída no console)
python cli.py coleta --modo atual > /dev/null 2>&1
```

## Automação de Coleta

Para garantir a coleta regular de dados, você pode automatizar o processo usando ferramentas do sistema operacional.

### No Linux ou macOS (usando cron)

1. Abra o editor crontab:
   ```bash
   crontab -e
   ```

2. Adicione linhas para execução programada:
   ```
   # Coletar dados atuais diariamente às 02:00
   0 2 * * * cd /caminho/completo/para/sistema_dados_climaticos && python cli.py coleta --modo atual > /dev/null 2>&1

   # Coletar dados históricos semanalmente aos domingos às 03:00
   0 3 * * 0 cd /caminho/completo/para/sistema_dados_climaticos && python cli.py coleta --modo historico > /dev/null 2>&1
   ```

3. Salve e feche o editor

### No Windows (usando Agendador de Tarefas)

1. Crie um arquivo batch `coletar_dados.bat`:
   ```batch
   @echo off
   cd C:\caminho\para\sistema_dados_climaticos
   python cli.py coleta --modo atual
   ```

2. Abra o Agendador de Tarefas do Windows:
   - Pesquise por "Agendador de Tarefas" no menu Iniciar
   - Clique em "Criar Tarefa Básica"
   - Defina um nome como "Coleta Diária de Dados Climáticos"
   - Escolha "Diariamente" e defina o horário para 02:00
   - Selecione "Iniciar um programa" e navegue até o arquivo .bat criado
   - Conclua o assistente

Repita o processo para a coleta histórica semanal se necessário.

## Perguntas Frequentes

### Perguntas Gerais

**P: Quantas regiões posso monitorar simultaneamente?**  
R: Tecnicamente, não há limite fixo, mas recomendamos até 50 regiões para manter um bom desempenho e não exceder limites de API. As APIs gratuitas têm limites diários de requisições.

**P: Os dados são atualizados automaticamente?**  
R: Não. Você precisa iniciar a coleta manualmente ou configurar automação usando cron ou Agendador de Tarefas.

**P: Posso usar o sistema offline?**  
R: Parcialmente. A coleta de novos dados requer conexão à internet, mas a análise de dados já coletados funciona offline.

**P: Como faço para atualizar o sistema?**  
R: Use git para atualizar os arquivos (`git pull`), depois execute o script de instalação novamente para atualizar dependências.

### Questões Técnicas

**P: Como alterar o período de dados históricos?**  
R: Por padrão, o sistema coleta até 15 anos de dados históricos. Você pode alterar isso usando o parâmetro `--anos` no modo de comando.

**P: É possível exportar dados para outras ferramentas como PowerBI?**  
R: Sim. Exporte os dados em formato CSV, que pode ser importado pela maioria das ferramentas de análise.

**P: Ocorreu um erro "chave API inválida" mesmo com a chave correta. O que fazer?**  
R: Verifique se a chave foi ativada (pode levar algumas horas após o cadastro). Tente usar a chave diretamente no navegador para confirmar que está funcionando.

**P: Os logs estão ocupando muito espaço. Como limpar?**  
R: Use a função "Limpar logs antigos" no menu "Logs e Monitoramento" do CLI.

## Solução de Problemas

### Problemas Comuns e Soluções

#### Falhas na Coleta de Dados

**Problema**: Erro "API key not valid" ao coletar dados
**Solução**: 
1. Verifique se digitou a chave corretamente
2. Confirme se a chave está ativa na sua conta OpenWeather
3. Aguarde algumas horas após criar uma nova chave
4. Tente a coleta com a API secundária (INMET)

**Problema**: Erro "Não foi possível obter dados para [região]"
**Solução**:
1. Verifique sua conexão com a internet
2. Confirme se as coordenadas da região estão corretas
3. Verifique os logs para mensagens de erro detalhadas
4. Tente coletar novamente mais tarde (pode ser um problema temporário da API)

#### Problemas de Visualização

**Problema**: Gráficos não são exibidos
**Solução**:
1. Confirme que o matplotlib está instalado (`pip install matplotlib`)
2. Verifique se há dados disponíveis para o período selecionado
3. Tente um período diferente ou outra região

**Problema**: Erro ao exportar para Excel
**Solução**: 
1. Instale a biblioteca opcional openpyxl: `pip install openpyxl`
2. Verifique permissões de escrita no diretório de destino

#### Problemas de Sistema

**Problema**: Mensagem "Diretório não encontrado"
**Solução**: Use o menu "Verificar diretórios do sistema" para identificar e criar diretórios ausentes

**Problema**: Erro "ModuleNotFoundError" ao iniciar o sistema
**Solução**: Reinstale as dependências com `pip install -r requisitos.txt`

### Verificação do Sistema

Se encontrar problemas, execute estas verificações básicas:

1. **Verifique as dependências**:
   ```bash
   pip install -r requisitos.txt
   ```

2. **Verifique os diretórios**:
   ```bash
   python cli.py
   # Selecione: Configurações > Verificar diretórios do sistema
   ```

3. **Verifique os logs**:
   ```bash
   python cli.py
   # Selecione: Logs e Monitoramento > Visualizar logs do sistema
   ```

4. **Verifique as credenciais**:
   ```bash
   python cli.py
   # Selecione: Configurações > Configurar credenciais de API
   ```

## Suporte e Contato

### Como Obter Ajuda

Se você encontrar problemas não resolvidos nesta documentação:

1. **Consulte os logs**: A maioria dos erros será registrada nos arquivos de log
2. **Verifique as Perguntas Frequentes** neste documento
3. **Reporte problemas** no repositório do GitHub
4. **Entre em contato** com a equipe de suporte

### Contato

- **Email de Suporte**: suporte@exemplo.com.br
- **Repositório GitHub**: github.com/seuusuario/sistema_dados_climaticos
- **Documentação Online**: docs.exemplo.com/sistema_climatico