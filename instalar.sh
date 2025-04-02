#!/bin/bash

# Script de instalação para o sistema de coleta de dados climáticos

echo "Instalando o Sistema de Coleta de Dados Climáticos..."

# Verificar se Python 3 está instalado
if command -v python3 &>/dev/null; then
    echo "Python 3 encontrado"
else
    echo "Python 3 não encontrado. Por favor, instale o Python 3 primeiro."
    exit 1
fi

# Verificar se pip está instalado
if command -v pip3 &>/dev/null; then
    echo "pip encontrado"
else
    echo "pip não encontrado. Instalando pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    rm get-pip.py
fi

# Criar ambiente virtual (opcional)
echo "Criando ambiente virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
echo "Instalando dependências..."
pip install -r requisitos.txt

# Verificar se inmetpy deve ser instalado
echo "Deseja instalar a biblioteca inmetpy para acesso à API do INMET?"
echo "1. Sim"
echo "2. Não"
read -p "Escolha uma opção [1]: " opcao_inmet
opcao_inmet=${opcao_inmet:-1}

if [[ $opcao_inmet == "1" ]]; then
    echo "Instalando inmetpy..."
    pip install inmetpy
fi

# Criar diretórios necessários
echo "Criando estrutura de diretórios..."
mkdir -p dados/openweather
mkdir -p dados/inmet
mkdir -p logs

# Configuração das credenciais
echo "Configurando credenciais de API..."
mkdir -p config

# Criar arquivo de credenciais se não existir
if [ ! -f config/credenciais.json ]; then
    echo '{
  "openweather": {
    "api_key": ""
  },
  "inmet": {
    "token": ""
  }
}' > config/credenciais.json
fi

# Configuração do token INMET (opcional)
echo "Você possui um token do INMET?"
echo "1. Sim"
echo "2. Não"
read -p "Escolha uma opção [2]: " opcao_token
opcao_token=${opcao_token:-2}

if [[ $opcao_token == "1" ]]; then
    read -p "Digite seu token do INMET: " token_inmet
    # Atualizar o token no arquivo de configuração
    # Usando temp file para compatibilidade com diferentes sistemas
    jq --arg token "$token_inmet" '.inmet.token = $token' config/credenciais.json > config/credenciais.json.tmp
    mv config/credenciais.json.tmp config/credenciais.json
    echo "Token INMET configurado."
fi

# Configuração da chave OpenWeather (se necessário)
echo "Deseja atualizar a chave API do OpenWeather?"
echo "1. Sim"
echo "2. Não"
read -p "Escolha uma opção [2]: " opcao_api
opcao_api=${opcao_api:-2}

if [[ $opcao_api == "1" ]]; then
    read -p "Digite sua chave API do OpenWeather: " chave_ow
    # Atualizar a chave no arquivo de configuração
    jq --arg key "$chave_ow" '.openweather.api_key = $key' config/credenciais.json > config/credenciais.json.tmp
    mv config/credenciais.json.tmp config/credenciais.json
    echo "Chave API OpenWeather configurada."
fi

# Configurar permissão de execução
chmod +x coletor_climatico.py
chmod +x analisador_dados.py

echo ""
echo "Instalação concluída!"
echo ""
echo "Para coletar dados atuais, execute:"
echo "python coletor_climatico.py --modo atual"
echo ""
echo "Para analisar os dados coletados, execute:"
echo "python analisador_dados.py --regiao NOME_REGIAO"
echo ""
echo "Para listar regiões disponíveis:"
echo "python analisador_dados.py --listar-regioes"
echo ""

# Perguntar se deseja configurar cron
echo "Deseja configurar a execução automática diária?"
echo "1. Sim"
echo "2. Não"
read -p "Escolha uma opção [2]: " opcao_cron
opcao_cron=${opcao_cron:-2}

if [[ $opcao_cron == "1" ]]; then
    # Obter caminho absoluto
    DIR_SCRIPT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
    
    # Criar entrada cron
    ENTRADA_CRON="0 2 * * * cd $DIR_SCRIPT && ./venv/bin/python coletor_climatico.py --modo atual"
    
    # Verificar se a entrada já existe
    CRON_EXISTENTE=$(crontab -l 2>/dev/null | grep -F "$DIR_SCRIPT")
    
    if [ -z "$CRON_EXISTENTE" ]; then
        # Adicionar ao crontab
        (crontab -l 2>/dev/null; echo "$ENTRADA_CRON") | crontab -
        echo "Execução automática configurada para todos os dias às 2:00 AM."
    else
        echo "Uma entrada cron para este script já existe. Configuração manual necessária."
    fi
fi