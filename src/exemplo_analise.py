#!/usr/bin/env python3
"""
Exemplo de análise de dados climáticos utilizando Pandas e Matplotlib.
Este script demonstra como carregar e visualizar os dados coletados pelo sistema.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime, timedelta
import glob

# Configurações para gráficos mais bonitos
plt.style.use('ggplot')
sns.set(style="darkgrid")

# Diretório de dados
DIRETORIO_DADOS = Path(__file__).parent.parent / "dados"

def listar_regioes_disponiveis():
    """Lista todas as regiões com dados disponíveis"""
    regioes = set()
    
    # Buscar em ambas as fontes de dados
    for fonte in ['openweather', 'inmet']:
        padrao_busca = str(DIRETORIO_DADOS / fonte / "**" / "*.csv")
        for arquivo in glob.glob(padrao_busca, recursive=True):
            nome_arquivo = os.path.basename(arquivo)
            if nome_arquivo.startswith(("atual_", "historico_")):
                partes = nome_arquivo.split("_")
                if len(partes) >= 3:
                    # O formato esperado é tipo_regiao_data.csv ou tipo_regiao_parte1_parte2_data.csv
                    if partes[0] in ["atual", "historico"]:
                        # Para regiões com nomes compostos (ex: Sao_Paulo_SP)
                        # vamos extrair tudo entre o primeiro _ e o último _
                        primeiro_indice = nome_arquivo.find('_') + 1
                        ultimo_indice = nome_arquivo.rfind('_')
                        regiao = nome_arquivo[primeiro_indice:ultimo_indice]
                        regioes.add(regiao)
    
    return sorted(list(regioes))

def carregar_dados(regiao, tipo="atual", dias=30):
    """
    Carrega os dados de uma região específica.
    
    Args:
        regiao: Nome da região
        tipo: 'atual' ou 'historico'
        dias: Número de dias a considerar (para tipo 'atual')
        
    Returns:
        DataFrame com os dados combinados ou None se não encontrar
    """
    todos_dados = []
    
    # Data limite para filtragem
    data_limite = datetime.now() - timedelta(days=dias)
    
    # Buscar primeiro em OpenWeather, depois em INMET
    for fonte in ['openweather', 'inmet']:
        padrao_busca = str(DIRETORIO_DADOS / fonte / "**" / f"{tipo}_{regiao}_*.csv")
        arquivos = glob.glob(padrao_busca, recursive=True)
        
        for arquivo in sorted(arquivos, reverse=True):  # Mais recentes primeiro
            df = pd.read_csv(arquivo)
            
            # Adicionar metadados se não existir
            if 'fonte' not in df.columns:
                df['fonte'] = fonte
            if 'regiao' not in df.columns:
                df['regiao'] = regiao
                
            # Processar datas
            if fonte == 'openweather' and 'data' in df.columns and 'hora' in df.columns:
                df['data_hora'] = pd.to_datetime(df['data'] + ' ' + df['hora'])
            elif fonte == 'inmet' and 'DATETIME' in df.columns:
                df['data_hora'] = pd.to_datetime(df['DATETIME'])
            
            # Filtrar por data se necessário
            if 'data_hora' in df.columns and tipo == 'atual':
                df = df[df['data_hora'] >= data_limite]
            
            if not df.empty:
                todos_dados.append(df)
    
    if not todos_dados:
        print(f"Nenhum dado encontrado para {regiao} (tipo: {tipo})")
        return None
    
    # Combinar todos os DataFrames
    dados_combinados = pd.concat(todos_dados, ignore_index=True)
    
    # Remover duplicatas por data/hora se houver
    if 'data_hora' in dados_combinados.columns:
        dados_combinados = dados_combinados.drop_duplicates(subset=['data_hora'])
        dados_combinados = dados_combinados.sort_values('data_hora')
    
    return dados_combinados

def analisar_temperatura(dados, regiao, salvar=False):
    """Análise e visualização de temperatura"""
    if dados is None or dados.empty:
        print("Sem dados para análise de temperatura")
        return
    
    plt.figure(figsize=(12, 8))
    
    # Determinar colunas de temperatura com base na fonte
    if 'temperatura' in dados.columns:
        # OpenWeather
        if 'data_hora' in dados.columns:
            plt.plot(dados['data_hora'], dados['temperatura'], 'r-', linewidth=2, 
                     label='Temperatura (°C)')
            
            # Adicionar min/max se disponíveis
            if 'temp_min' in dados.columns and 'temp_max' in dados.columns:
                plt.fill_between(dados['data_hora'], 
                                dados['temp_min'], 
                                dados['temp_max'], 
                                alpha=0.2, color='red',
                                label='Faixa (min-max)')
        
    elif 'TEM_INS' in dados.columns:
        # INMET
        if 'data_hora' in dados.columns:
            plt.plot(dados['data_hora'], dados['TEM_INS'], 'r-', linewidth=2, 
                    label='Temperatura (°C)')
    
    plt.title(f'Análise de Temperatura - {regiao.replace("_", " ")}', fontsize=16)
    plt.xlabel('Data', fontsize=12)
    plt.ylabel('Temperatura (°C)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=12)
    
    # Ajustar eixo x para melhor visualização
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    
    if salvar:
        plt.savefig(f'temperatura_{regiao}.png', dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo como temperatura_{regiao}.png")
    else:
        plt.show()
    
    # Estatísticas básicas
    print("\n=== Estatísticas de Temperatura ===")
    if 'temperatura' in dados.columns:
        estatisticas = dados['temperatura'].describe()
    elif 'TEM_INS' in dados.columns:
        estatisticas = dados['TEM_INS'].describe()
    else:
        return
    
    print(f"Média: {estatisticas['mean']:.1f}°C")
    print(f"Mínima: {estatisticas['min']:.1f}°C")
    print(f"Máxima: {estatisticas['max']:.1f}°C")
    print(f"Desvio Padrão: {estatisticas['std']:.1f}°C")

def analisar_precipitacao(dados, regiao, salvar=False):
    """Análise e visualização de precipitação"""
    if dados is None or dados.empty:
        print("Sem dados para análise de precipitação")
        return
    
    coluna_chuva = None
    
    if 'chuva_1h' in dados.columns:
        coluna_chuva = 'chuva_1h'
    elif 'CHUVA' in dados.columns:
        coluna_chuva = 'CHUVA'
    
    if coluna_chuva is None:
        print("Dados de precipitação não disponíveis")
        return
    
    plt.figure(figsize=(12, 8))
    
    if 'data_hora' in dados.columns:
        # Gráfico de barras para precipitação
        plt.bar(dados['data_hora'], dados[coluna_chuva], width=0.01, 
                color='blue', alpha=0.7, label='Precipitação (mm)')
    
    plt.title(f'Análise de Precipitação - {regiao.replace("_", " ")}', fontsize=16)
    plt.xlabel('Data', fontsize=12)
    plt.ylabel('Precipitação (mm)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=12)
    
    # Ajustar eixo x para melhor visualização
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    
    if salvar:
        plt.savefig(f'precipitacao_{regiao}.png', dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo como precipitacao_{regiao}.png")
    else:
        plt.show()
    
    # Estatísticas básicas
    print("\n=== Estatísticas de Precipitação ===")
    estatisticas = dados[coluna_chuva].describe()
    
    print(f"Total: {dados[coluna_chuva].sum():.1f} mm")
    print(f"Média: {estatisticas['mean']:.1f} mm")
    print(f"Máxima: {estatisticas['max']:.1f} mm")
    dias_com_chuva = (dados[coluna_chuva] > 0).sum()
    print(f"Dias com chuva: {dias_com_chuva}")

def analisar_correlacao(dados, regiao, salvar=False):
    """Análise de correlação entre variáveis climáticas"""
    if dados is None or dados.empty:
        print("Sem dados para análise de correlação")
        return
    
    # Identificar colunas numéricas relevantes
    colunas_numericas = []
    
    # Mapear colunas para OpenWeather
    if 'temperatura' in dados.columns:
        colunas_interesse = ['temperatura', 'umidade', 'pressao', 
                            'velocidade_vento', 'nuvens']
        for col in colunas_interesse:
            if col in dados.columns:
                colunas_numericas.append(col)
    
    # Mapear colunas para INMET
    elif 'TEM_INS' in dados.columns:
        colunas_mapeamento = {
            'TEM_INS': 'Temperatura',
            'UMD_INS': 'Umidade',
            'PRE_INS': 'Pressão',
            'VEN_VEL': 'Vel. Vento',
            'CHUVA': 'Precipitação',
            'RAD_GLO': 'Radiação'
        }
        
        for col_original, nome in colunas_mapeamento.items():
            if col_original in dados.columns:
                # Renomear para facilitar a análise
                dados[nome] = dados[col_original]
                colunas_numericas.append(nome)
    
    if len(colunas_numericas) < 2:
        print("Dados insuficientes para análise de correlação")
        return
    
    # Calcular matriz de correlação
    corr_matrix = dados[colunas_numericas].corr()
    
    # Plotar heatmap de correlação
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5, 
                vmin=-1, vmax=1, center=0, fmt='.2f')
    plt.title(f'Correlação entre Variáveis Climáticas - {regiao.replace("_", " ")}', fontsize=16)
    plt.tight_layout()
    
    if salvar:
        plt.savefig(f'correlacao_{regiao}.png', dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo como correlacao_{regiao}.png")
    else:
        plt.show()
    
    # Insight sobre correlações fortes
    print("\n=== Correlações Significativas ===")
    for i in range(len(colunas_numericas)):
        for j in range(i+1, len(colunas_numericas)):
            corr = corr_matrix.iloc[i, j]
            if abs(corr) > 0.5:  # Considerando correlações moderadas a fortes
                print(f"{colunas_numericas[i]} e {colunas_numericas[j]}: {corr:.2f}")

def main():
    """Função principal para demonstração"""
    print("=== Sistema de Análise de Dados Climáticos ===\n")
    
    # Listar regiões disponíveis
    regioes = listar_regioes_disponiveis()
    if not regioes:
        print("Nenhuma região com dados encontrada. Execute a coleta primeiro.")
        return
    
    print("Regiões disponíveis:")
    for i, regiao in enumerate(regioes, 1):
        print(f"{i}. {regiao.replace('_', ' ')}")
    
    try:
        escolha = int(input("\nEscolha uma região (número): ")) - 1
        if escolha < 0 or escolha >= len(regioes):
            print("Opção inválida.")
            return
        
        regiao_escolhida = regioes[escolha]
        print(f"\nAnalisando dados climáticos para: {regiao_escolhida.replace('_', ' ')}")
        
        # Escolher tipo de dados
        tipo = input("\nTipo de dados (atual/historico) [atual]: ").lower() or "atual"
        if tipo not in ["atual", "historico"]:
            print("Tipo inválido. Usando 'atual'.")
            tipo = "atual"
        
        # Carregar dados
        dados = carregar_dados(regiao_escolhida, tipo=tipo)
        
        if dados is None:
            print(f"Não foram encontrados dados do tipo '{tipo}' para {regiao_escolhida}.")
            return
        
        print(f"\nDados carregados: {len(dados)} registros.")
        
        # Menu de análises
        while True:
            print("\nOpções de análise:")
            print("1. Análise de temperatura")
            print("2. Análise de precipitação")
            print("3. Correlação entre variáveis")
            print("4. Visualizar dados brutos (primeiras linhas)")
            print("5. Salvar todas as análises como imagens")
            print("0. Sair")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "1":
                analisar_temperatura(dados, regiao_escolhida)
            elif opcao == "2":
                analisar_precipitacao(dados, regiao_escolhida)
            elif opcao == "3":
                analisar_correlacao(dados, regiao_escolhida)
            elif opcao == "4":
                print("\n=== Primeiras linhas de dados ===")
                print(dados.head())
                print("\nColunas disponíveis:", list(dados.columns))
            elif opcao == "5":
                print("\nSalvando todas as análises...")
                analisar_temperatura(dados, regiao_escolhida, salvar=True)
                analisar_precipitacao(dados, regiao_escolhida, salvar=True)
                analisar_correlacao(dados, regiao_escolhida, salvar=True)
                print("Análises salvas no diretório atual.")
            elif opcao == "0":
                break
            else:
                print("Opção inválida!")
    
    except Exception as e:
        print(f"Erro durante a análise: {str(e)}")

if __name__ == "__main__":
    main()