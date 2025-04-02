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
read -p "Deseja instalar a biblioteca inmetpy para acesso à API do INMET? (s/n): " instalar_inmet
if [[ $instalar_inmet == "s" || $instalar_inmet == "S" ]]; then
    echo "Instalando inmetpy..."
    pip install inmetpy
fi

# Criar diretórios necessários
echo "Criando estrutura de diretórios..."
mkdir -p dados/openweather
mkdir -p dados/inmet
mkdir -p logs

# Configuração do token INMET (opcional)
read -p "Você possui um token do INMET? (s/n): " tem_token
if [[ $tem_token == "s" || $tem_token == "S" ]]; then
    read -p "Digite seu token do INMET: " token_inmet
    # Atualizar o token no arquivo Python
    sed -i "s/TOKEN_INMET = \"seu_token_aqui\"/TOKEN_INMET = \"$token_inmet\"/" coletor_climatico.py
    echo "Token INMET configurado."
fi

# Configuração da chave OpenWeather (se necessário)
read -p "Deseja atualizar a chave API do OpenWeather? (s/n): " atualizar_chave
if [[ $atualizar_chave == "s" || $atualizar_chave == "S" ]]; then
    read -p "Digite sua chave API do OpenWeather: " chave_ow
    # Atualizar a chave no arquivo Python
    sed -i "s/CHAVE_API_OPENWEATHER = \"0476cdfcc3da9e85452287b12c174cf1\"/CHAVE_API_OPENWEATHER = \"$chave_ow\"/" coletor_climatico.py
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
read -p "Deseja configurar a execução automática diária? (s/n): " configurar_cron
if [[ $configurar_cron == "s" || $configurar_cron == "S" ]]; then
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