# Sistema de Coleta de Dados Climáticos

Sistema para coleta e análise de dados climáticos de diversas fontes (OpenWeather e INMET), com failover automático, gerenciamento de regiões e visualização de dados. Projetado para uso em modelos preditivos de demanda agrícola.

![Licença](https://img.shields.io/badge/licença-MIT-blue)
![Versão](https://img.shields.io/badge/versão-1.0.0-green)

## 🌦️ Visão Geral

O Sistema de Dados Climáticos é uma aplicação que automatiza a coleta, armazenamento e análise de dados meteorológicos para regiões agrícolas do Brasil. Ele utiliza múltiplas APIs como fontes de dados (OpenWeather como principal e INMET como backup), permitindo tanto análises em tempo real quanto históricas.

## ✨ Principais Funcionalidades

- **Coleta Automática**: Dados atuais (últimos 7 dias) e históricos (até 15 anos)
- **Múltiplas Fontes**: OpenWeather (principal) e INMET (backup) com failover automático
- **Gerenciamento de Regiões**: Interface para configurar e gerenciar as regiões monitoradas
- **Análise de Dados**: Visualização de temperatura, precipitação, umidade e correlações
- **Exportação de Dados**: Formatos CSV, Excel e gráficos
- **Interface Completa**: CLI interativo com menus intuitivos e modo de comando

## 🚀 Instalação

### Pré-requisitos

- Python 3.7+
- pip (gerenciador de pacotes Python)
- Conexão com a internet para acesso às APIs

### Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/seuusuario/sistema_dados_climaticos.git
cd sistema_dados_climaticos

# Instale as dependências
pip install -r requisitos.txt

# Execute o script de instalação para configurar o ambiente
chmod +x instalar.sh
./instalar.sh
```

### Configuração de APIs

Você precisará de chaves de API para:

1. **OpenWeather**: Obtenha uma chave em [openweathermap.org](https://openweathermap.org/api)
2. **INMET** (opcional): Obtenha um token em [portal.inmet.gov.br](https://portal.inmet.gov.br/)

Configure suas chaves usando o CLI:
```bash
python cli.py
# Selecione: Configurações > Configurar credenciais de API
```

## 🖥️ Como Usar

### Interface Interativa

A maneira mais simples de usar o sistema é através da interface interativa:

```bash
python cli.py
```

### Modo de Comando

Para automação e scripts:

```bash
# Coleta de dados atuais
python cli.py coleta --modo atual

# Coleta de dados históricos
python cli.py coleta --modo historico

# Coleta para regiões específicas
python cli.py coleta --regioes Ribeirao_Preto_SP Brasilia_DF

# Análise interativa
python cli.py analise
```

## 📊 Exemplos de Visualização

O sistema gera visualizações de alta qualidade para análise de dados climáticos:

- Gráficos de temperatura
- Históricos de precipitação
- Padrões de umidade
- Gráficos de correlação entre variáveis

## 📂 Estrutura de Diretórios

```
sistema_dados_climaticos/
├── cli.py                  # Interface de linha de comando
├── src/                    # Código-fonte
│   ├── coletor_climatico.py  # Coleta de dados
│   ├── analisador_dados.py   # Análise e visualização
│   └── ...
├── config/                 # Arquivos de configuração
├── dados/                  # Dados coletados (organizados por fonte/ano/mês)
├── logs/                   # Logs de execução (organizados por ano/mês)
├── docs/                   # Documentação
├── requisitos.txt          # Dependências Python
└── instalar.sh             # Script de instalação
```

## 📚 Documentação

Para instruções detalhadas sobre todas as funcionalidades, consulte:

- [Manual do Usuário](docs/DOCUMENTACAO.md): Guia completo para usuários
- [Ajuda no CLI]: Execute `python cli.py ajuda` para documentação interativa

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do repositório
2. Crie um branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para o branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto é licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📧 Contato

Para suporte, sugestões ou feedback:
- Email: suporte@exemplo.com.br
- Issues: Abra um issue no GitHub