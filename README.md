# Sistema de Coleta de Dados Climáticos

Sistema para coleta de dados climáticos do OpenWeather (principal) e INMET (backup) 
com failover automático, projetado para uso em modelos preditivos de demanda agrícola.

## Funcionalidades

- ✅ Coleta de dados atuais (últimos 7 dias)
- ✅ Coleta de dados históricos (últimos 15 anos)
- ✅ Failover automático entre APIs
- ✅ Sistema de logs detalhado
- ✅ Prevenção de duplicação de dados
- ✅ Verificação de consistência dos dados
- ✅ Estrutura organizada por região e data
- ✅ Configuração externa de regiões
- ✅ Interface de linha de comando (CLI)

## Requisitos

```bash
pip install -r requisitos.txt
```

## Estrutura de Diretórios

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

## Uso do CLI

A maneira mais fácil de usar o sistema é através do CLI interativo:

```bash
python cli.py
```

### Interface Interativa

A interface interativa oferece um menu completo com todas as funcionalidades:

- Coleta de dados (atual/histórico/ambos)
- Consulta e análise de dados
- Gerenciamento de regiões
- Exportação de dados para CSV/Excel
- Visualização de logs
- Configurações das APIs

### Modo de Comando

O sistema também pode ser executado em modo de comando para automação:

```bash
# Coleta de dados atuais
python cli.py coleta --modo atual

# Coleta de dados históricos
python cli.py coleta --modo historico

# Coleta para regiões específicas
python cli.py coleta --regioes Ribeirao_Preto_SP Brasilia_DF

# Iniciar análise interativa
python cli.py analise
```

## Configuração de Regiões

As regiões monitoradas são definidas no arquivo `config/regioes.json`. Você pode gerenciar as regiões através do CLI:

1. Execute o CLI e selecione "Gerenciar Regiões"
2. Use as opções para adicionar, remover ou importar regiões de CSV

## Documentação Completa

Para instruções detalhadas sobre instalação, configuração, automação e solução de problemas, consulte o arquivo [docs/DOCUMENTACAO.md](docs/DOCUMENTACAO.md) ou acesse a ajuda no CLI.