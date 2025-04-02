"""
Utilitário para análise básica dos dados coletados pelo sistema de coleta climática.
Permite visualizar gráficos de temperatura, umidade e precipitação.
"""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import glob
from pathlib import Path
from datetime import datetime, timedelta


def listar_regioes_disponiveis():
    """Lista todas as regiões disponíveis nos dados coletados."""
    caminho_base = Path(__file__).parent.parent / "dados"
    
    regioes = set()
    
    # Procurar em OpenWeather
    for arquivo_csv in glob.glob(str(caminho_base / "openweather" / "**" / "*.csv"), recursive=True):
        nome_arquivo = os.path.basename(arquivo_csv)
        if nome_arquivo.startswith("atual_"):
            regiao = nome_arquivo.split("_", 1)[1].rsplit("_", 1)[0]
            regioes.add(regiao)
    
    # Procurar em INMET
    for arquivo_csv in glob.glob(str(caminho_base / "inmet" / "**" / "*.csv"), recursive=True):
        nome_arquivo = os.path.basename(arquivo_csv)
        if nome_arquivo.startswith("atual_"):
            regiao = nome_arquivo.split("_", 1)[1].rsplit("_", 1)[0]
            regioes.add(regiao)
    
    return sorted(list(regioes))


def carregar_dados_recentes(regiao, dias=7):
    """
    Carrega os dados recentes de uma região específica.
    
    Args:
        regiao (str): Nome da região
        dias (int): Número de dias para carregar
        
    Returns:
        pd.DataFrame: DataFrame combinado com dados da região
    """
    caminho_base = Path(__file__).parent.parent / "dados"
    hoje = datetime.now()
    
    # Calcular intervalo de datas
    intervalo_datas = [(hoje - timedelta(days=i)).strftime("%Y%m%d") for i in range(dias)]
    
    # Procurar arquivos que correspondem à região e datas
    todos_dados = []
    
    # Primeiro OpenWeather
    for data_str in intervalo_datas:
        ano = data_str[:4]
        mes = data_str[4:6]
        padrao_arquivo = f"atual_{regiao}_{data_str}.csv"
        
        # Caminho para OpenWeather
        caminho_ow = caminho_base / "openweather" / ano / mes / padrao_arquivo
        if caminho_ow.exists():
            df = pd.read_csv(caminho_ow)
            todos_dados.append(df)
            continue  # Se tiver dados OpenWeather, não precisa do INMET
        
        # Caminho para INMET (backup)
        caminho_inmet = caminho_base / "inmet" / ano / mes / padrao_arquivo
        if caminho_inmet.exists():
            df = pd.read_csv(caminho_inmet)
            todos_dados.append(df)
    
    if not todos_dados:
        print(f"Nenhum dado encontrado para a região {regiao} nos últimos {dias} dias.")
        return None
    
    # Combinar todos os DataFrames
    dados_combinados = pd.concat(todos_dados, ignore_index=True)
    
    # Processar datas
    if 'data' in dados_combinados.columns and 'hora' in dados_combinados.columns:
        # Dados OpenWeather
        dados_combinados['datetime'] = pd.to_datetime(dados_combinados['data'] + ' ' + dados_combinados['hora'])
    elif 'DATETIME' in dados_combinados.columns:
        # Dados INMET
        dados_combinados['datetime'] = pd.to_datetime(dados_combinados['DATETIME'])
    else:
        print("Formato de data não reconhecido nos dados.")
        return dados_combinados
    
    # Ordenar por data
    return dados_combinados.sort_values('datetime')


def plotar_temperatura(dados, regiao, caminho_salvar=None):
    """
    Plota gráfico de temperatura para uma região.
    
    Args:
        dados (pd.DataFrame): DataFrame com os dados
        regiao (str): Nome da região
        caminho_salvar (str, optional): Caminho para salvar o gráfico
    """
    plt.figure(figsize=(12, 6))
    
    if 'temperatura' in dados.columns:
        # OpenWeather
        coluna_temp = 'temperatura'
    elif 'TEM_INS' in dados.columns:
        # INMET
        coluna_temp = 'TEM_INS'
    else:
        print("Coluna de temperatura não encontrada nos dados.")
        return
    
    plt.plot(dados['datetime'], dados[coluna_temp], 'r-', label='Temperatura')
    
    # Adicionar min/max se disponível
    if 'temp_min' in dados.columns and 'temp_max' in dados.columns:
        plt.plot(dados['datetime'], dados['temp_min'], 'b--', alpha=0.5, label='Mínima')
        plt.plot(dados['datetime'], dados['temp_max'], 'r--', alpha=0.5, label='Máxima')
    
    plt.title(f'Temperatura em {regiao.replace("_", " ")}')
    plt.xlabel('Data')
    plt.ylabel('Temperatura (°C)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Formatar eixo x para melhor visualização de datas
    plt.gcf().autofmt_xdate()
    
    if caminho_salvar:
        plt.savefig(caminho_salvar)
        print(f"Gráfico salvo em: {caminho_salvar}")
    else:
        # Salvar no diretório Downloads do usuário se não for especificado
        diretorio = os.path.join(os.path.expanduser("~"), "Downloads")
        if not os.path.exists(diretorio):
            print("Pasta Downloads não encontrada. Mostrando gráfico sem salvar.")
            plt.tight_layout()
            plt.show()
        else:
            # Criar nome de arquivo com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            caminho_arquivo = os.path.join(diretorio, f'temperatura_{regiao}_{timestamp}.png')
            plt.savefig(caminho_arquivo)
            print(f"Gráfico salvo em: {caminho_arquivo}")
            plt.tight_layout()
            plt.show()


def plotar_umidade(dados, regiao, caminho_salvar=None):
    """
    Plota gráfico de umidade para uma região.
    
    Args:
        dados (pd.DataFrame): DataFrame com os dados
        regiao (str): Nome da região
        caminho_salvar (str, optional): Caminho para salvar o gráfico
    """
    plt.figure(figsize=(12, 6))
    
    if 'umidade' in dados.columns:
        # OpenWeather
        coluna_umidade = 'umidade'
    elif 'UMD_INS' in dados.columns:
        # INMET
        coluna_umidade = 'UMD_INS'
    else:
        print("Coluna de umidade não encontrada nos dados.")
        return
    
    plt.plot(dados['datetime'], dados[coluna_umidade], 'b-', label='Umidade')
    
    plt.title(f'Umidade em {regiao.replace("_", " ")}')
    plt.xlabel('Data')
    plt.ylabel('Umidade (%)')
    plt.ylim(0, 100)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Formatar eixo x para melhor visualização de datas
    plt.gcf().autofmt_xdate()
    
    if caminho_salvar:
        plt.savefig(caminho_salvar)
        print(f"Gráfico salvo em: {caminho_salvar}")
    else:
        # Salvar no diretório Downloads do usuário se não for especificado
        diretorio = os.path.join(os.path.expanduser("~"), "Downloads")
        if not os.path.exists(diretorio):
            print("Pasta Downloads não encontrada. Mostrando gráfico sem salvar.")
            plt.tight_layout()
            plt.show()
        else:
            # Criar nome de arquivo com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            caminho_arquivo = os.path.join(diretorio, f'umidade_{regiao}_{timestamp}.png')
            plt.savefig(caminho_arquivo)
            print(f"Gráfico salvo em: {caminho_arquivo}")
            plt.tight_layout()
            plt.show()


def plotar_precipitacao(dados, regiao, caminho_salvar=None):
    """
    Plota gráfico de precipitação para uma região.
    
    Args:
        dados (pd.DataFrame): DataFrame com os dados
        regiao (str): Nome da região
        caminho_salvar (str, optional): Caminho para salvar o gráfico
    """
    plt.figure(figsize=(12, 6))
    
    coluna_chuva = None
    
    # Verificar qual coluna usar para precipitação
    if 'chuva_1h' in dados.columns:
        # OpenWeather
        coluna_chuva = 'chuva_1h'
    elif 'CHUVA' in dados.columns:
        # INMET
        coluna_chuva = 'CHUVA'
    
    if coluna_chuva is None:
        print("Coluna de precipitação não encontrada nos dados.")
        return
    
    plt.bar(dados['datetime'], dados[coluna_chuva], width=0.02, color='blue', alpha=0.7)
    
    plt.title(f'Precipitação em {regiao.replace("_", " ")}')
    plt.xlabel('Data')
    plt.ylabel('Precipitação (mm)')
    plt.grid(True, alpha=0.3)
    
    # Formatar eixo x para melhor visualização de datas
    plt.gcf().autofmt_xdate()
    
    if caminho_salvar:
        plt.savefig(caminho_salvar)
        print(f"Gráfico salvo em: {caminho_salvar}")
    else:
        # Salvar no diretório Downloads do usuário se não for especificado
        diretorio = os.path.join(os.path.expanduser("~"), "Downloads")
        if not os.path.exists(diretorio):
            print("Pasta Downloads não encontrada. Mostrando gráfico sem salvar.")
            plt.tight_layout()
            plt.show()
        else:
            # Criar nome de arquivo com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            caminho_arquivo = os.path.join(diretorio, f'precipitacao_{regiao}_{timestamp}.png')
            plt.savefig(caminho_arquivo)
            print(f"Gráfico salvo em: {caminho_arquivo}")
            plt.tight_layout()
            plt.show()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Analisador de Dados Climáticos")
    parser.add_argument('--listar-regioes', action='store_true', help='Listar regiões disponíveis')
    parser.add_argument('--regiao', type=str, help='Nome da região para análise')
    parser.add_argument('--dias', type=int, default=7, help='Número de dias para análise')
    parser.add_argument('--grafico', choices=['temp', 'umidade', 'chuva', 'todos'], 
                        default='todos', help='Tipo de gráfico a gerar')
    parser.add_argument('--salvar-dir', type=str, help='Diretório para salvar gráficos')
    
    args = parser.parse_args()
    
    if args.listar_regioes:
        regioes = listar_regioes_disponiveis()
        if regioes:
            print("\nRegiões disponíveis:")
            for regiao in regioes:
                print(f"  - {regiao}")
        else:
            print("\nNenhuma região encontrada. Execute a coleta de dados primeiro.")
        sys.exit(0)
    
    if not args.regiao:
        print("Erro: Especifique uma região com --regiao ou liste regiões disponíveis com --listar-regioes")
        sys.exit(1)
    
    # Carregar dados
    dados = carregar_dados_recentes(args.regiao, args.dias)
    
    if dados is None or len(dados) == 0:
        print(f"Nenhum dado encontrado para a região {args.regiao}.")
        sys.exit(1)
    
    # Configurar diretório para salvar
    diretorio_salvar = None
    if args.salvar_dir:
        diretorio_salvar = Path(args.salvar_dir)
        diretorio_salvar.mkdir(exist_ok=True, parents=True)
    
    # Gerar gráficos
    if args.grafico in ['temp', 'todos']:
        caminho_temp = None
        if diretorio_salvar:
            caminho_temp = diretorio_salvar / f"temperatura_{args.regiao}.png"
        plotar_temperatura(dados, args.regiao, caminho_temp)
    
    if args.grafico in ['umidade', 'todos']:
        caminho_umidade = None
        if diretorio_salvar:
            caminho_umidade = diretorio_salvar / f"umidade_{args.regiao}.png"
        plotar_umidade(dados, args.regiao, caminho_umidade)
    
    if args.grafico in ['chuva', 'todos']:
        caminho_chuva = None
        if diretorio_salvar:
            caminho_chuva = diretorio_salvar / f"precipitacao_{args.regiao}.png"
        plotar_precipitacao(dados, args.regiao, caminho_chuva)
    
    # Se não estiver salvando, mostra os gráficos interativamente
    if not args.salvar_dir and args.grafico == 'todos':
        plt.show()
    
    print(f"\nAnálise de {args.regiao} concluída.")