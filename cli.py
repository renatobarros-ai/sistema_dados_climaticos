#!/usr/bin/env python3
"""
Interface de linha de comando (CLI) para o Sistema de Dados Climáticos.
Este script fornece uma interface amigável para todas as funcionalidades do sistema.
"""

import os
import sys
import json
import csv
import logging
import argparse
import webbrowser
import pandas as pd
from datetime import datetime
from pathlib import Path
from tabulate import tabulate
from colorama import init, Fore, Style
import matplotlib.pyplot as plt

# Inicializar colorama para cores no terminal
init(autoreset=True)

# Configuração de diretórios
BASE_DIR = Path(__file__).parent
SRC_DIR = BASE_DIR / "src"
CONFIG_DIR = BASE_DIR / "config"
DADOS_DIR = BASE_DIR / "dados"
LOGS_DIR = BASE_DIR / "logs"
DOCS_DIR = BASE_DIR / "docs"
TEMP_DIR = BASE_DIR / "temp"

# Garantir que os diretórios existam
TEMP_DIR.mkdir(exist_ok=True, parents=True)

# Adicionar diretório src ao path para importar módulos
sys.path.append(str(SRC_DIR))

# Criar um logger para o CLI
# Organizar logs por ano/mês, semelhante aos dados
hoje = datetime.now()
diretorio_log_ano = LOGS_DIR / str(hoje.year)
diretorio_log_mes = diretorio_log_ano / f"{hoje.month:02d}"

# Criar diretórios de log se não existirem
diretorio_log_ano.mkdir(exist_ok=True, parents=True)
diretorio_log_mes.mkdir(exist_ok=True, parents=True)

arquivo_log = diretorio_log_mes / f"cli_{hoje.strftime('%Y%m%d')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(arquivo_log),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("cli")

# Banner ASCII do sistema
BANNER = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   {Fore.YELLOW}███████╗██████╗  ██████╗    ██████╗██╗     ██╗███╗   ███╗{Fore.CYAN}   ║
║   {Fore.YELLOW}██╔════╝██╔══██╗██╔════╝   ██╔════╝██║     ██║████╗ ████║{Fore.CYAN}   ║
║   {Fore.YELLOW}███████╗██║  ██║██║        ██║     ██║     ██║██╔████╔██║{Fore.CYAN}   ║
║   {Fore.YELLOW}╚════██║██║  ██║██║        ██║     ██║     ██║██║╚██╔╝██║{Fore.CYAN}   ║
║   {Fore.YELLOW}███████║██████╔╝╚██████╗   ╚██████╗███████╗██║██║ ╚═╝ ██║{Fore.CYAN}   ║
║   {Fore.YELLOW}╚══════╝╚═════╝  ╚═════╝    ╚═════╝╚══════╝╚═╝╚═╝     ╚═╝{Fore.CYAN}   ║
║                                                               ║
║     {Fore.GREEN}Sistema de Dados Climáticos - v1.0.0{Fore.CYAN}                  ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""


def print_header(texto):
    """Imprime um cabeçalho formatado na tela"""
    largura = 70
    print("\n" + "=" * largura)
    print(f"{Fore.CYAN}{texto.center(largura)}{Style.RESET_ALL}")
    print("=" * largura + "\n")


def print_info(texto):
    """Imprime informação formatada na tela"""
    print(f"{Fore.GREEN}ℹ {texto}{Style.RESET_ALL}")


def print_warning(texto):
    """Imprime aviso formatado na tela"""
    print(f"{Fore.YELLOW}⚠ {texto}{Style.RESET_ALL}")


def print_error(texto):
    """Imprime erro formatado na tela"""
    print(f"{Fore.RED}✖ {texto}{Style.RESET_ALL}")


def print_success(texto):
    """Imprime mensagem de sucesso formatada na tela"""
    print(f"{Fore.GREEN}✓ {texto}{Style.RESET_ALL}")


def print_table(data, headers):
    """Imprime uma tabela formatada na tela"""
    print(tabulate(data, headers=headers, tablefmt="grid"))


def clear_screen():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    """Pausa a execução até o usuário pressionar ENTER"""
    input(f"\n{Fore.YELLOW}Pressione ENTER para continuar...{Style.RESET_ALL}")


def confirm_action(mensagem="Confirma esta ação?"):
    """Solicita confirmação do usuário para uma ação"""
    resposta = input(f"{Fore.YELLOW}{mensagem} (s/n): {Style.RESET_ALL}").lower()
    return resposta in ['s', 'sim', 'y', 'yes']


def mostrar_menu_principal():
    """Exibe o menu principal do sistema"""
    clear_screen()
    print(BANNER)
    print_header("MENU PRINCIPAL")
    print(f"{Fore.CYAN}1.{Style.RESET_ALL} Coleta de Dados")
    print(f"{Fore.CYAN}2.{Style.RESET_ALL} Consulta e Análise")
    print(f"{Fore.CYAN}3.{Style.RESET_ALL} Gerenciar Regiões")
    print(f"{Fore.CYAN}4.{Style.RESET_ALL} Exportação de Dados")
    print(f"{Fore.CYAN}5.{Style.RESET_ALL} Logs e Monitoramento")
    print(f"{Fore.CYAN}6.{Style.RESET_ALL} Configurações")
    print(f"{Fore.CYAN}7.{Style.RESET_ALL} Ajuda e Documentação")
    print(f"{Fore.CYAN}0.{Style.RESET_ALL} Sair")
    print()
    return input("Escolha uma opção: ")


def executar_coleta(modo="atual", regioes=None, dias=7, anos=15):
    """
    Executa a coleta de dados climáticos
    
    Args:
        modo: 'atual', 'historico' ou 'ambos'
        regioes: lista de nomes de regiões (opcional)
        dias: número de dias para coleta atual
        anos: número de anos para coleta histórica
    """
    from src.executar_coleta import main as executar_coleta_main
    
    cmd_args = ["--modo", modo]
    
    if regioes:
        cmd_args.extend(["--regioes"] + regioes)
    if dias != 7:
        cmd_args.extend(["--dias", str(dias)])
    if anos != 15:
        cmd_args.extend(["--anos", str(anos)])
    
    # Salvar os argumentos originais
    original_args = sys.argv.copy()
    
    try:
        # Substituir sys.argv com nossos argumentos
        sys.argv = [sys.argv[0]] + cmd_args
        print_info(f"Executando coleta com argumentos: {' '.join(cmd_args)}")
        executar_coleta_main()
        print_success("Coleta concluída com sucesso!")
    except Exception as e:
        print_error(f"Erro ao executar coleta: {e}")
        logger.exception("Erro na execução da coleta")
    finally:
        # Restaurar argumentos originais
        sys.argv = original_args


def menu_coleta():
    """Menu de coleta de dados"""
    while True:
        clear_screen()
        print_header("COLETA DE DADOS")
        print(f"{Fore.CYAN}1.{Style.RESET_ALL} Coletar dados atuais (últimos 7 dias)")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} Coletar dados históricos")
        print(f"{Fore.CYAN}3.{Style.RESET_ALL} Coletar todos os dados (atual + histórico)")
        print(f"{Fore.CYAN}4.{Style.RESET_ALL} Coletar dados para região específica")
        print(f"{Fore.CYAN}0.{Style.RESET_ALL} Voltar")
        print()
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            print_info("Iniciando coleta de dados atuais...")
            executar_coleta(modo="atual")
            pause()
        elif opcao == "2":
            print_info("Iniciando coleta de dados históricos...")
            executar_coleta(modo="historico")
            pause()
        elif opcao == "3":
            print_info("Iniciando coleta completa de dados...")
            executar_coleta(modo="ambos")
            pause()
        elif opcao == "4":
            # Obter lista de regiões disponíveis
            regioes = listar_regioes_configuradas()
            
            if not regioes:
                print_warning("Nenhuma região configurada encontrada!")
                pause()
                continue
            
            print_header("REGIÕES DISPONÍVEIS")
            for i, regiao in enumerate(regioes, 1):
                print(f"{Fore.CYAN}{i}.{Style.RESET_ALL} {regiao}")
            print()
            
            try:
                escolha = input("Escolha uma região (número) ou ENTER para todas: ")
                if escolha.strip():
                    indice = int(escolha) - 1
                    if 0 <= indice < len(regioes):
                        regiao_escolhida = [regioes[indice]]
                        print_info(f"Região selecionada: {regiao_escolhida[0]}")
                    else:
                        print_error("Índice inválido!")
                        pause()
                        continue
                else:
                    regiao_escolhida = None
                
                # Escolher tipo de dados com menu numérico
                print("\nTipo de dados:")
                print(f"{Fore.CYAN}1.{Style.RESET_ALL} Dados atuais (últimos dias)")
                print(f"{Fore.CYAN}2.{Style.RESET_ALL} Dados históricos (anos anteriores)")
                print(f"{Fore.CYAN}3.{Style.RESET_ALL} Ambos (atual + histórico)")
                
                opcao_tipo = input("\nEscolha uma opção [1]: ") or "1"
                
                if opcao_tipo == "1":
                    modo = "atual"
                elif opcao_tipo == "2":
                    modo = "historico"
                elif opcao_tipo == "3":
                    modo = "ambos"
                else:
                    print_warning("Opção inválida. Usando 'atual'.")
                    modo = "atual"
                
                # Executar coleta para a região específica
                executar_coleta(modo=modo, regioes=regiao_escolhida)
                
            except ValueError:
                print_error("Entrada inválida!")
            
            pause()
        elif opcao == "0":
            break
        else:
            print_warning("Opção inválida!")
            pause()


def listar_regioes_configuradas():
    """Obtém a lista de regiões configuradas no sistema"""
    try:
        with open(CONFIG_DIR / "regioes.json", "r", encoding="utf-8") as f:
            dados = json.load(f)
            regioes = [r["nome"] for r in dados.get("regioes_agricolas", [])]
            return regioes
    except Exception as e:
        logger.error(f"Erro ao carregar regiões: {e}")
        return []


def listar_regioes_com_dados():
    """Lista todas as regiões que possuem dados coletados"""
    from src.analisador_dados import listar_regioes_disponiveis
    return listar_regioes_disponiveis()


def visualizar_dados(regiao, tipo="atual"):
    """Visualiza dados de uma região específica"""
    from src.analisador_dados import carregar_dados_recentes
    
    print_info(f"Carregando dados {tipo} para {regiao}...")
    
    try:
        # Carregar dados
        dados = carregar_dados_recentes(regiao, dias=30 if tipo == "atual" else 365)
        
        if dados is None or dados.empty:
            print_error(f"Nenhum dado encontrado para {regiao}!")
            return
        
        # Mostrar estatísticas básicas
        print_success(f"{len(dados)} registros encontrados")
        
        # Detectar colunas importantes com base na fonte
        colunas_temperatura = [c for c in dados.columns if "temp" in c.lower()]
        colunas_umidade = [c for c in dados.columns if "umid" in c.lower() or c == "UMD_INS"]
        colunas_chuva = [c for c in dados.columns if "chuva" in c.lower() or "rain" in c.lower() or c == "CHUVA"]
        
        # Mostrar as primeiras linhas
        print("\nPrimeiras linhas dos dados:")
        print(tabulate(dados.head(5).to_dict('records'), headers="keys", tablefmt="grid"))
        
        # Estatísticas descritivas
        if colunas_temperatura:
            print("\nEstatísticas de temperatura:")
            stats = dados[colunas_temperatura[0]].describe()
            print(f"  Média: {stats['mean']:.1f}°C")
            print(f"  Mínima: {stats['min']:.1f}°C")
            print(f"  Máxima: {stats['max']:.1f}°C")
        
        if colunas_umidade:
            print("\nEstatísticas de umidade:")
            stats = dados[colunas_umidade[0]].describe()
            print(f"  Média: {stats['mean']:.1f}%")
            print(f"  Mínima: {stats['min']:.1f}%")
            print(f"  Máxima: {stats['max']:.1f}%")
        
        if colunas_chuva:
            print("\nEstatísticas de precipitação:")
            total = dados[colunas_chuva[0]].sum()
            print(f"  Total: {total:.1f}mm")
            dias_com_chuva = (dados[colunas_chuva[0]] > 0).sum()
            print(f"  Dias com chuva: {dias_com_chuva}")
        
        # Perguntar se deseja visualizar gráficos
        print("\nDeseja visualizar gráficos?")
        print(f"{Fore.CYAN}1.{Style.RESET_ALL} Sim")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} Não")
        opcao_graficos = input("Escolha uma opção [1]: ") or "1"
        
        if opcao_graficos == "1":
            from src.analisador_dados import plotar_temperatura, plotar_umidade, plotar_precipitacao
            
            print("\nQual gráfico deseja visualizar?")
            print(f"{Fore.CYAN}1.{Style.RESET_ALL} Temperatura")
            print(f"{Fore.CYAN}2.{Style.RESET_ALL} Umidade")
            print(f"{Fore.CYAN}3.{Style.RESET_ALL} Precipitação")
            print(f"{Fore.CYAN}4.{Style.RESET_ALL} Todos os gráficos")
            opcao_grafico = input("Escolha uma opção [4]: ") or "4"
            
            if opcao_grafico == "1" and colunas_temperatura:
                plotar_temperatura(dados, regiao)
            elif opcao_grafico == "2" and colunas_umidade:
                plotar_umidade(dados, regiao)
            elif opcao_grafico == "3" and colunas_chuva:
                plotar_precipitacao(dados, regiao)
            else:  # Opção 4 ou inválida: mostrar todos
                if colunas_temperatura:
                    plotar_temperatura(dados, regiao)
                if colunas_umidade:
                    plotar_umidade(dados, regiao)
                if colunas_chuva:
                    plotar_precipitacao(dados, regiao)
            
            plt.show()
    
    except Exception as e:
        print_error(f"Erro ao visualizar dados: {e}")
        logger.exception("Erro na visualização de dados")


def menu_consulta():
    """Menu de consulta e análise de dados"""
    while True:
        clear_screen()
        print_header("CONSULTA E ANÁLISE DE DADOS")
        print(f"{Fore.CYAN}1.{Style.RESET_ALL} Listar regiões com dados disponíveis")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} Visualizar dados de uma região")
        print(f"{Fore.CYAN}3.{Style.RESET_ALL} Visualizar dados históricos")
        print(f"{Fore.CYAN}4.{Style.RESET_ALL} Análise avançada (interface interativa)")
        print(f"{Fore.CYAN}5.{Style.RESET_ALL} Comparar regiões")
        print(f"{Fore.CYAN}0.{Style.RESET_ALL} Voltar")
        print()
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            regioes = listar_regioes_com_dados()
            print_header("REGIÕES COM DADOS")
            
            if regioes:
                for i, regiao in enumerate(regioes, 1):
                    print(f"{Fore.CYAN}{i}.{Style.RESET_ALL} {regiao}")
            else:
                print_warning("Nenhuma região com dados encontrada. Execute a coleta primeiro.")
            
            pause()
        
        elif opcao == "2" or opcao == "3":
            # Dados atuais ou históricos
            tipo = "historico" if opcao == "3" else "atual"
            
            # Listar regiões disponíveis
            regioes = listar_regioes_com_dados()
            
            if not regioes:
                print_warning("Nenhuma região com dados encontrada. Execute a coleta primeiro.")
                pause()
                continue
            
            print_header("REGIÕES COM DADOS")
            for i, regiao in enumerate(regioes, 1):
                print(f"{Fore.CYAN}{i}.{Style.RESET_ALL} {regiao}")
            print()
            
            try:
                escolha = int(input("Escolha uma região (número): "))
                if 1 <= escolha <= len(regioes):
                    regiao = regioes[escolha - 1]
                    visualizar_dados(regiao, tipo)
                else:
                    print_error("Índice inválido!")
            except ValueError:
                print_error("Entrada inválida!")
            
            pause()
        
        elif opcao == "4":
            # Interface interativa de análise
            print_info("Iniciando interface interativa de análise...")
            try:
                # Usar subprocess para manter o CLI responsivo
                import subprocess
                subprocess.run([sys.executable, str(SRC_DIR / "exemplo_analise.py")])
            except Exception as e:
                print_error(f"Erro ao iniciar interface de análise: {e}")
            
            pause()
        
        elif opcao == "5":
            # Comparar regiões
            regioes = listar_regioes_com_dados()
            
            if len(regioes) < 2:
                print_warning("É necessário ter pelo menos duas regiões com dados para comparação.")
                pause()
                continue
            
            print_header("COMPARAÇÃO DE REGIÕES")
            print_info("Selecione duas regiões para comparar:")
            
            for i, regiao in enumerate(regioes, 1):
                print(f"{Fore.CYAN}{i}.{Style.RESET_ALL} {regiao}")
            print()
            
            try:
                escolha1 = int(input("Primeira região (número): "))
                escolha2 = int(input("Segunda região (número): "))
                
                if 1 <= escolha1 <= len(regioes) and 1 <= escolha2 <= len(regioes) and escolha1 != escolha2:
                    regiao1 = regioes[escolha1 - 1]
                    regiao2 = regioes[escolha2 - 1]
                    
                    # Implementar comparação de regiões
                    print_info(f"Comparando {regiao1} e {regiao2}...")
                    
                    # Aqui você pode implementar a lógica de comparação ou chamar uma função
                    # Por exemplo, plotar temperatura das duas regiões no mesmo gráfico
                    from src.analisador_dados import carregar_dados_recentes
                    
                    dados1 = carregar_dados_recentes(regiao1, dias=30)
                    dados2 = carregar_dados_recentes(regiao2, dias=30)
                    
                    if dados1 is None or dados2 is None or dados1.empty or dados2.empty:
                        print_error("Dados insuficientes para comparação!")
                    else:
                        # Identificar coluna de temperatura
                        col_temp1 = next((c for c in dados1.columns if "temp" in c.lower()), None)
                        col_temp2 = next((c for c in dados2.columns if "temp" in c.lower()), None)
                        
                        if col_temp1 and col_temp2 and 'datetime' in dados1.columns and 'datetime' in dados2.columns:
                            plt.figure(figsize=(12, 6))
                            plt.plot(dados1['datetime'], dados1[col_temp1], 'r-', label=regiao1)
                            plt.plot(dados2['datetime'], dados2[col_temp2], 'b-', label=regiao2)
                            plt.title(f'Comparação de Temperatura: {regiao1} vs {regiao2}')
                            plt.xlabel('Data')
                            plt.ylabel('Temperatura (°C)')
                            plt.legend()
                            plt.grid(True, alpha=0.3)
                            plt.gcf().autofmt_xdate()
                            plt.show()
                        else:
                            print_error("Não foi possível encontrar colunas compatíveis para comparação")
                else:
                    print_error("Seleção inválida!")
            except ValueError:
                print_error("Entrada inválida!")
            except Exception as e:
                print_error(f"Erro na comparação: {e}")
                logger.exception("Erro na comparação de regiões")
            
            pause()
        
        elif opcao == "0":
            break
        else:
            print_warning("Opção inválida!")
            pause()


def adicionar_regiao():
    """Adiciona uma nova região ao arquivo de configuração"""
    print_header("ADICIONAR NOVA REGIÃO")
    
    try:
        # Carregar regiões existentes
        with open(CONFIG_DIR / "regioes.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        
        # Verificar duplicação
        regioes_existentes = [r["nome"] for r in config.get("regioes_agricolas", [])]
        
        # Solicitar dados da nova região
        nome = input("Nome da região (sem espaços, ex: Sao_Paulo_SP): ")
        
        # Validar nome
        if not nome or " " in nome:
            print_error("O nome não pode conter espaços. Use underscores (_).")
            return
        
        # Verificar duplicação
        if nome in regioes_existentes:
            print_error(f"Já existe uma região com o nome '{nome}'")
            return
        
        descricao = input("Descrição (ex: Região de São Paulo - SP): ")
        
        try:
            latitude = float(input("Latitude (ex: -23.55): "))
            longitude = float(input("Longitude (ex: -46.64): "))
        except ValueError:
            print_error("Latitude e longitude devem ser números decimais!")
            return
        
        estacao_inmet = input("Código da estação INMET (ex: A701): ")
        
        # Criar objeto da nova região
        nova_regiao = {
            "nome": nome,
            "descricao": descricao,
            "latitude": latitude,
            "longitude": longitude,
            "estacao_inmet": estacao_inmet
        }
        
        # Adicionar à configuração
        if "regioes_agricolas" not in config:
            config["regioes_agricolas"] = []
        
        config["regioes_agricolas"].append(nova_regiao)
        
        # Salvar arquivo atualizado
        with open(CONFIG_DIR / "regioes.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print_success(f"Região '{nome}' adicionada com sucesso!")
    
    except Exception as e:
        print_error(f"Erro ao adicionar região: {e}")
        logger.exception("Erro ao adicionar região")


def remover_regiao():
    """Remove uma região do arquivo de configuração"""
    print_header("REMOVER REGIÃO")
    
    try:
        # Carregar regiões existentes
        with open(CONFIG_DIR / "regioes.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        
        regioes = config.get("regioes_agricolas", [])
        
        if not regioes:
            print_warning("Não há regiões configuradas para remover.")
            return
        
        print("Regiões disponíveis:")
        for i, regiao in enumerate(regioes, 1):
            print(f"{Fore.CYAN}{i}.{Style.RESET_ALL} {regiao['nome']} - {regiao['descricao']}")
        print()
        
        try:
            escolha = int(input("Escolha uma região para remover (número): "))
            if 1 <= escolha <= len(regioes):
                regiao = regioes[escolha - 1]
                nome_regiao = regiao["nome"]
                
                if confirm_action(f"Confirma a remoção da região '{nome_regiao}'?"):
                    config["regioes_agricolas"].pop(escolha - 1)
                    
                    # Salvar arquivo atualizado
                    with open(CONFIG_DIR / "regioes.json", "w", encoding="utf-8") as f:
                        json.dump(config, f, indent=2, ensure_ascii=False)
                    
                    print_success(f"Região '{nome_regiao}' removida com sucesso!")
            else:
                print_error("Índice inválido!")
        except ValueError:
            print_error("Entrada inválida!")
    
    except Exception as e:
        print_error(f"Erro ao remover região: {e}")
        logger.exception("Erro ao remover região")


def importar_regioes_csv():
    """Importa regiões a partir de um arquivo CSV"""
    print_header("IMPORTAR REGIÕES DE CSV")
    
    try:
        # Solicitar caminho do arquivo
        caminho = input("Caminho do arquivo CSV: ")
        
        if not os.path.exists(caminho):
            print_error(f"O arquivo '{caminho}' não existe!")
            return
        
        # Carregar configuração atual
        with open(CONFIG_DIR / "regioes.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        
        if "regioes_agricolas" not in config:
            config["regioes_agricolas"] = []
        
        regioes_existentes = [r["nome"] for r in config["regioes_agricolas"]]
        
        # Ler arquivo CSV
        with open(caminho, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            if not reader.fieldnames:
                print_error("Arquivo CSV vazio ou inválido!")
                return
            
            # Verificar campos necessários
            campos_necessarios = ["nome", "latitude", "longitude"]
            campos_faltantes = [campo for campo in campos_necessarios if campo not in reader.fieldnames]
            
            if campos_faltantes:
                print_error(f"Campos obrigatórios faltando no CSV: {', '.join(campos_faltantes)}")
                print_info(f"Campos disponíveis: {', '.join(reader.fieldnames)}")
                return
            
            # Processar linhas
            contador = 0
            for row in reader:
                # Verificar se região já existe
                if row["nome"] in regioes_existentes:
                    print_warning(f"Região '{row['nome']}' já existe e será ignorada.")
                    continue
                
                try:
                    # Criar objeto da nova região
                    nova_regiao = {
                        "nome": row["nome"],
                        "descricao": row.get("descricao", row["nome"]),
                        "latitude": float(row["latitude"]),
                        "longitude": float(row["longitude"]),
                        "estacao_inmet": row.get("estacao_inmet", "")
                    }
                    
                    # Adicionar à configuração
                    config["regioes_agricolas"].append(nova_regiao)
                    regioes_existentes.append(row["nome"])
                    contador += 1
                
                except (ValueError, KeyError) as e:
                    print_warning(f"Erro ao processar linha: {e}")
            
            # Salvar arquivo atualizado
            with open(CONFIG_DIR / "regioes.json", "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print_success(f"{contador} regiões importadas com sucesso!")
    
    except Exception as e:
        print_error(f"Erro ao importar regiões: {e}")
        logger.exception("Erro ao importar regiões")


def exportar_regioes_csv():
    """Exporta as regiões configuradas para um arquivo CSV"""
    print_header("EXPORTAR REGIÕES PARA CSV")
    
    try:
        # Carregar regiões existentes
        with open(CONFIG_DIR / "regioes.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        
        regioes = config.get("regioes_agricolas", [])
        
        if not regioes:
            print_warning("Não há regiões configuradas para exportar.")
            return
        
        # Solicitar caminho para salvar
        caminho = input("Caminho para salvar o arquivo CSV: ")
        
        # Verificar se é um diretório
        if os.path.isdir(caminho):
            caminho = os.path.join(caminho, "regioes_exportadas.csv")
        
        # Escrever arquivo CSV
        with open(caminho, 'w', encoding='utf-8', newline='') as csvfile:
            fieldnames = ["nome", "descricao", "latitude", "longitude", "estacao_inmet"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for regiao in regioes:
                writer.writerow({
                    "nome": regiao["nome"],
                    "descricao": regiao.get("descricao", ""),
                    "latitude": regiao["latitude"],
                    "longitude": regiao["longitude"],
                    "estacao_inmet": regiao.get("estacao_inmet", "")
                })
        
        print_success(f"{len(regioes)} regiões exportadas para '{caminho}'")
    
    except Exception as e:
        print_error(f"Erro ao exportar regiões: {e}")
        logger.exception("Erro ao exportar regiões")


def menu_regioes():
    """Menu de gerenciamento de regiões"""
    while True:
        clear_screen()
        print_header("GERENCIAR REGIÕES")
        print(f"{Fore.CYAN}1.{Style.RESET_ALL} Listar regiões configuradas")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} Adicionar nova região")
        print(f"{Fore.CYAN}3.{Style.RESET_ALL} Remover região")
        print(f"{Fore.CYAN}4.{Style.RESET_ALL} Importar regiões de CSV")
        print(f"{Fore.CYAN}5.{Style.RESET_ALL} Exportar regiões para CSV")
        print(f"{Fore.CYAN}0.{Style.RESET_ALL} Voltar")
        print()
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            regioes = listar_regioes_configuradas()
            
            print_header("REGIÕES CONFIGURADAS")
            
            if regioes:
                # Carregar detalhes das regiões
                with open(CONFIG_DIR / "regioes.json", "r", encoding="utf-8") as f:
                    config = json.load(f)
                
                regioes_info = []
                for regiao in config.get("regioes_agricolas", []):
                    regioes_info.append([
                        regiao["nome"],
                        regiao.get("descricao", ""),
                        regiao["latitude"],
                        regiao["longitude"],
                        regiao.get("estacao_inmet", "")
                    ])
                
                print_table(regioes_info, ["Nome", "Descrição", "Latitude", "Longitude", "Estação INMET"])
            else:
                print_warning("Nenhuma região configurada encontrada!")
            
            pause()
        
        elif opcao == "2":
            adicionar_regiao()
            pause()
        
        elif opcao == "3":
            remover_regiao()
            pause()
        
        elif opcao == "4":
            importar_regioes_csv()
            pause()
        
        elif opcao == "5":
            exportar_regioes_csv()
            pause()
        
        elif opcao == "0":
            break
        else:
            print_warning("Opção inválida!")
            pause()


def exportar_dados_csv(regiao, periodo="ultimo_mes"):
    """Exporta dados de uma região para CSV"""
    print_header(f"EXPORTAR DADOS DE {regiao.upper()}")
    
    try:
        from src.analisador_dados import carregar_dados_recentes
        
        # Determinar período
        dias = 30
        if periodo == "ultimo_ano":
            dias = 365
        elif periodo == "ultimos_3_meses":
            dias = 90
        elif periodo == "ultima_semana":
            dias = 7
        elif periodo == "ultimos_5_anos":
            dias = 365 * 5
        elif periodo == "todos_dados":
            dias = 365 * 15  # Até 15 anos
        
        # Carregar dados
        dados = carregar_dados_recentes(regiao, dias=dias)
        
        if dados is None or dados.empty:
            print_error(f"Nenhum dado encontrado para {regiao}!")
            return
        
        # Usando pasta Downloads do usuário para salvar
        diretorio = os.path.join(os.path.expanduser("~"), "Downloads")
        
        # Verificar se existe a pasta Downloads, caso contrário usar o diretório atual
        if not os.path.exists(diretorio):
            print_warning(f"Pasta Downloads não encontrada. Usando diretório atual.")
            diretorio = os.getcwd()
        
        # Criar nome de arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"{regiao}_{periodo}_{timestamp}.csv"
        caminho_completo = os.path.join(diretorio, nome_arquivo)
        
        # Salvar arquivo
        dados.to_csv(caminho_completo, index=False)
        
        print_success(f"{len(dados)} registros exportados para '{caminho_completo}'")
    
    except Exception as e:
        print_error(f"Erro ao exportar dados: {e}")
        logger.exception("Erro ao exportar dados")


def menu_exportacao():
    """Menu de exportação de dados"""
    while True:
        clear_screen()
        print_header("EXPORTAÇÃO DE DADOS")
        print(f"{Fore.CYAN}1.{Style.RESET_ALL} Exportar dados para CSV")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} Exportar dados para Excel")
        print(f"{Fore.CYAN}3.{Style.RESET_ALL} Exportar gráficos")
        print(f"{Fore.CYAN}0.{Style.RESET_ALL} Voltar")
        print()
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            # Listar regiões disponíveis
            regioes = listar_regioes_com_dados()
            
            if not regioes:
                print_warning("Nenhuma região com dados encontrada. Execute a coleta primeiro.")
                pause()
                continue
            
            print_header("EXPORTAR PARA CSV - REGIÕES DISPONÍVEIS")
            for i, regiao in enumerate(regioes, 1):
                print(f"{Fore.CYAN}{i}.{Style.RESET_ALL} {regiao}")
            print()
            
            try:
                escolha = int(input("Escolha uma região (número): "))
                if 1 <= escolha <= len(regioes):
                    regiao = regioes[escolha - 1]
                    
                    print("\nSelecione o período:")
                    print(f"{Fore.CYAN}1.{Style.RESET_ALL} Última semana")
                    print(f"{Fore.CYAN}2.{Style.RESET_ALL} Último mês")
                    print(f"{Fore.CYAN}3.{Style.RESET_ALL} Últimos 3 meses")
                    print(f"{Fore.CYAN}4.{Style.RESET_ALL} Último ano")
                    print(f"{Fore.CYAN}5.{Style.RESET_ALL} Últimos 5 anos")
                    print(f"{Fore.CYAN}6.{Style.RESET_ALL} Todos os dados (até 15 anos)")
                    
                    periodo_opcao = input("\nEscolha uma opção [2]: ") or "2"
                    
                    periodo = "ultimo_mes"
                    if periodo_opcao == "1":
                        periodo = "ultima_semana"
                    elif periodo_opcao == "3":
                        periodo = "ultimos_3_meses"
                    elif periodo_opcao == "4":
                        periodo = "ultimo_ano"
                    elif periodo_opcao == "5":
                        periodo = "ultimos_5_anos"
                    elif periodo_opcao == "6":
                        periodo = "todos_dados"
                    
                    exportar_dados_csv(regiao, periodo)
                else:
                    print_error("Índice inválido!")
            except ValueError:
                print_error("Entrada inválida!")
            
            pause()
        
        elif opcao == "2":
            # Verificar se pandas pode exportar para Excel
            try:
                import pandas as pd
                exporta_excel = True
            except (ImportError, AttributeError):
                exporta_excel = False
            
            if not exporta_excel:
                print_error("Exportação para Excel não disponível. Instale as dependências necessárias.")
                print_info("Execute: pip install openpyxl pandas")
                pause()
                continue
            
            # Listar regiões disponíveis
            regioes = listar_regioes_com_dados()
            
            if not regioes:
                print_warning("Nenhuma região com dados encontrada. Execute a coleta primeiro.")
                pause()
                continue
            
            print_header("EXPORTAR PARA EXCEL - REGIÕES DISPONÍVEIS")
            for i, regiao in enumerate(regioes, 1):
                print(f"{Fore.CYAN}{i}.{Style.RESET_ALL} {regiao}")
            print()
            
            try:
                escolha = int(input("Escolha uma região (número): "))
                if 1 <= escolha <= len(regioes):
                    regiao = regioes[escolha - 1]
                    
                    # Carregar dados com opções de período
                    print("\nSelecione o período:")
                    print(f"{Fore.CYAN}1.{Style.RESET_ALL} Último mês")
                    print(f"{Fore.CYAN}2.{Style.RESET_ALL} Último ano")
                    print(f"{Fore.CYAN}3.{Style.RESET_ALL} Últimos 5 anos")
                    print(f"{Fore.CYAN}4.{Style.RESET_ALL} Todos os dados (até 15 anos)")
                    
                    periodo_opcao = input("\nEscolha uma opção [1]: ") or "1"
                    
                    dias = 30  # padrão: último mês
                    if periodo_opcao == "2":
                        dias = 365  # último ano
                    elif periodo_opcao == "3":
                        dias = 365 * 5  # últimos 5 anos
                    elif periodo_opcao == "4":
                        dias = 365 * 15  # todos os dados (até 15 anos)
                    
                    from src.analisador_dados import carregar_dados_recentes
                    dados = carregar_dados_recentes(regiao, dias=dias)
                    
                    if dados is None or dados.empty:
                        print_error(f"Nenhum dado encontrado para {regiao}!")
                        pause()
                        continue
                    
                    # Usando pasta Downloads do usuário para salvar
                    diretorio = os.path.join(os.path.expanduser("~"), "Downloads")
                    
                    # Verificar se existe a pasta Downloads, caso contrário usar o diretório atual
                    if not os.path.exists(diretorio):
                        print_warning(f"Pasta Downloads não encontrada. Usando diretório atual.")
                        diretorio = os.getcwd()
                    
                    # Criar nome de arquivo
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    nome_arquivo = f"{regiao}_dados_{timestamp}.xlsx"
                    caminho_completo = os.path.join(diretorio, nome_arquivo)
                    
                    # Salvar arquivo
                    dados.to_excel(caminho_completo, index=False, engine='openpyxl')
                    
                    print_success(f"{len(dados)} registros exportados para '{caminho_completo}'")
                else:
                    print_error("Índice inválido!")
            except ValueError:
                print_error("Entrada inválida!")
            except Exception as e:
                print_error(f"Erro ao exportar para Excel: {e}")
                logger.exception("Erro ao exportar para Excel")
            
            pause()
        
        elif opcao == "3":
            # Exportar gráficos
            regioes = listar_regioes_com_dados()
            
            if not regioes:
                print_warning("Nenhuma região com dados encontrada. Execute a coleta primeiro.")
                pause()
                continue
            
            print_header("EXPORTAR GRÁFICOS - REGIÕES DISPONÍVEIS")
            for i, regiao in enumerate(regioes, 1):
                print(f"{Fore.CYAN}{i}.{Style.RESET_ALL} {regiao}")
            print()
            
            try:
                escolha = int(input("Escolha uma região (número): "))
                if 1 <= escolha <= len(regioes):
                    regiao = regioes[escolha - 1]
                    
                    # Usando pasta Downloads do usuário para salvar
                    diretorio = os.path.join(os.path.expanduser("~"), "Downloads")
                    
                    # Verificar se existe a pasta Downloads, caso contrário usar o diretório atual
                    if not os.path.exists(diretorio):
                        print_warning(f"Pasta Downloads não encontrada. Usando diretório atual.")
                        diretorio = os.getcwd()
                    
                    # Carregar dados com opções de período
                    print("\nSelecione o período para análise:")
                    print(f"{Fore.CYAN}1.{Style.RESET_ALL} Último mês")
                    print(f"{Fore.CYAN}2.{Style.RESET_ALL} Último ano")
                    print(f"{Fore.CYAN}3.{Style.RESET_ALL} Últimos 5 anos")
                    print(f"{Fore.CYAN}4.{Style.RESET_ALL} Todos os dados (até 15 anos)")
                    
                    periodo_opcao = input("\nEscolha uma opção [1]: ") or "1"
                    
                    dias = 30  # padrão: último mês
                    if periodo_opcao == "2":
                        dias = 365  # último ano
                    elif periodo_opcao == "3":
                        dias = 365 * 5  # últimos 5 anos
                    elif periodo_opcao == "4":
                        dias = 365 * 15  # todos os dados (até 15 anos)
                    
                    from src.analisador_dados import carregar_dados_recentes
                    from src.analisador_dados import plotar_temperatura, plotar_umidade, plotar_precipitacao
                    
                    dados = carregar_dados_recentes(regiao, dias=dias)
                    
                    if dados is None or dados.empty:
                        print_error(f"Nenhum dado encontrado para {regiao}!")
                        pause()
                        continue
                    
                    # Timestamp para os arquivos
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    
                    # Salvar gráficos
                    print_info("Gerando gráficos...")
                    
                    # Temperatura
                    try:
                        arquivo_temp = os.path.join(diretorio, f"{regiao}_temperatura_{timestamp}.png")
                        plt.figure(figsize=(12, 8))
                        plotar_temperatura(dados, regiao, arquivo_temp)
                        print_success(f"Gráfico de temperatura salvo em '{arquivo_temp}'")
                    except Exception as e:
                        print_warning(f"Erro ao gerar gráfico de temperatura: {e}")
                    
                    # Umidade
                    try:
                        arquivo_umid = os.path.join(diretorio, f"{regiao}_umidade_{timestamp}.png")
                        plt.figure(figsize=(12, 8))
                        plotar_umidade(dados, regiao, arquivo_umid)
                        print_success(f"Gráfico de umidade salvo em '{arquivo_umid}'")
                    except Exception as e:
                        print_warning(f"Erro ao gerar gráfico de umidade: {e}")
                    
                    # Precipitação
                    try:
                        arquivo_chuva = os.path.join(diretorio, f"{regiao}_precipitacao_{timestamp}.png")
                        plt.figure(figsize=(12, 8))
                        plotar_precipitacao(dados, regiao, arquivo_chuva)
                        print_success(f"Gráfico de precipitação salvo em '{arquivo_chuva}'")
                    except Exception as e:
                        print_warning(f"Erro ao gerar gráfico de precipitação: {e}")
                
                else:
                    print_error("Índice inválido!")
            except ValueError:
                print_error("Entrada inválida!")
            except Exception as e:
                print_error(f"Erro ao exportar gráficos: {e}")
                logger.exception("Erro ao exportar gráficos")
            
            pause()
        
        elif opcao == "0":
            break
        else:
            print_warning("Opção inválida!")
            pause()


def visualizar_logs():
    """Visualiza os logs do sistema"""
    print_header("VISUALIZAR LOGS")
    
    # Listar todos os arquivos de log organizados por ano/mês
    arquivos_log = sorted(LOGS_DIR.glob("**/*.log"), key=os.path.getmtime, reverse=True)
    
    if not arquivos_log:
        print_warning("Nenhum arquivo de log encontrado.")
        return
    
    print("Arquivos de log disponíveis:")
    for i, arquivo in enumerate(arquivos_log, 1):
        tamanho = os.path.getsize(arquivo) / 1024  # KB
        data_mod = datetime.fromtimestamp(os.path.getmtime(arquivo)).strftime("%Y-%m-%d %H:%M:%S")
        print(f"{Fore.CYAN}{i}.{Style.RESET_ALL} {arquivo.name} ({tamanho:.1f} KB) - {data_mod}")
    print()
    
    try:
        escolha = int(input("Escolha um arquivo (número): "))
        if 1 <= escolha <= len(arquivos_log):
            arquivo = arquivos_log[escolha - 1]
            
            # Ler conteúdo do log
            with open(arquivo, "r", encoding="utf-8") as f:
                linhas = f.readlines()
            
            # Se o arquivo for muito grande, mostrar apenas as últimas 50 linhas
            if len(linhas) > 50:
                print_info(f"Arquivo grande ({len(linhas)} linhas). Mostrando as últimas 50 linhas.")
                linhas = linhas[-50:]
            
            print_header(f"CONTEÚDO DE {arquivo.name}")
            for linha in linhas:
                # Colorir linha de acordo com o nível de log
                if "ERROR" in linha:
                    print(f"{Fore.RED}{linha.strip()}{Style.RESET_ALL}")
                elif "WARNING" in linha:
                    print(f"{Fore.YELLOW}{linha.strip()}{Style.RESET_ALL}")
                elif "INFO" in linha:
                    print(f"{Fore.GREEN}{linha.strip()}{Style.RESET_ALL}")
                else:
                    print(linha.strip())
            
            # Perguntar se deseja exportar
            if input("\nDeseja exportar este log? (s/n) [n]: ").lower() == "s":
                diretorio = input("Diretório para salvar (ENTER para usar o diretório atual): ")
                
                if not diretorio:
                    diretorio = os.getcwd()
                
                if not os.path.exists(diretorio):
                    print_error(f"O diretório '{diretorio}' não existe!")
                    return
                
                # Copiar arquivo
                import shutil
                destino = os.path.join(diretorio, arquivo.name)
                shutil.copy2(arquivo, destino)
                
                print_success(f"Log exportado para '{destino}'")
        else:
            print_error("Índice inválido!")
    except ValueError:
        print_error("Entrada inválida!")
    except Exception as e:
        print_error(f"Erro ao visualizar log: {e}")
        logger.exception("Erro ao visualizar log")


def menu_logs():
    """Menu de logs e monitoramento"""
    while True:
        clear_screen()
        print_header("LOGS E MONITORAMENTO")
        print(f"{Fore.CYAN}1.{Style.RESET_ALL} Visualizar logs do sistema")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} Verificar estatísticas de coleta")
        print(f"{Fore.CYAN}3.{Style.RESET_ALL} Limpar logs antigos")
        print(f"{Fore.CYAN}0.{Style.RESET_ALL} Voltar")
        print()
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            visualizar_logs()
            pause()
        
        elif opcao == "2":
            print_header("ESTATÍSTICAS DE COLETA")
            
            # Contar arquivos por região
            dados_por_regiao = {}
            
            # Procurar no diretório de dados
            for fonte in ["openweather", "inmet"]:
                fonte_dir = DADOS_DIR / fonte
                if not fonte_dir.exists():
                    continue
                
                for arquivo in fonte_dir.glob("**/*.csv"):
                    nome_arquivo = arquivo.name
                    
                    # Extrair região do nome do arquivo
                    partes = nome_arquivo.split("_")
                    if len(partes) >= 3 and partes[0] in ["atual", "historico"]:
                        # Obter região a partir do nome do arquivo
                        # Formato: tipo_regiao_data.csv ou tipo_regiao_parte1_data.csv
                        primeiro_indice = nome_arquivo.find('_') + 1
                        ultimo_indice = nome_arquivo.rfind('_')
                        regiao = nome_arquivo[primeiro_indice:ultimo_indice]
                        
                        if regiao not in dados_por_regiao:
                            dados_por_regiao[regiao] = {"atual": 0, "historico": 0, "fonte": {}}
                        
                        # Adicionar a fonte
                        if fonte not in dados_por_regiao[regiao]["fonte"]:
                            dados_por_regiao[regiao]["fonte"][fonte] = 0
                        
                        dados_por_regiao[regiao]["fonte"][fonte] += 1
                        
                        # Incrementar contador por tipo
                        tipo = partes[0]  # "atual" ou "historico"
                        dados_por_regiao[regiao][tipo] += 1
            
            # Mostrar estatísticas
            if not dados_por_regiao:
                print_warning("Nenhum dado encontrado. Execute a coleta primeiro.")
            else:
                dados_tabela = []
                for regiao, stats in dados_por_regiao.items():
                    fontes = ", ".join(f"{f}: {c}" for f, c in stats["fonte"].items())
                    dados_tabela.append([
                        regiao,
                        stats["atual"],
                        stats["historico"],
                        fontes
                    ])
                
                print_table(dados_tabela, ["Região", "Atual", "Histórico", "Fontes"])
            
            pause()
        
        elif opcao == "3":
            print_header("LIMPAR LOGS ANTIGOS")
            
            # Listar todos os arquivos de log organizados por ano/mês
            arquivos_log = sorted(LOGS_DIR.glob("**/*.log"), key=os.path.getmtime)
            
            if not arquivos_log:
                print_warning("Nenhum arquivo de log encontrado.")
                pause()
                continue
            
            print_info(f"Existem {len(arquivos_log)} arquivos de log.")
            
            # Oferecer opções de limpeza
            print("\nOpções de limpeza:")
            print(f"{Fore.CYAN}1.{Style.RESET_ALL} Manter apenas os logs dos últimos 7 dias")
            print(f"{Fore.CYAN}2.{Style.RESET_ALL} Manter apenas os logs do último mês")
            print(f"{Fore.CYAN}3.{Style.RESET_ALL} Manter apenas os 10 logs mais recentes")
            print(f"{Fore.CYAN}4.{Style.RESET_ALL} Limpar todos os logs")
            print(f"{Fore.CYAN}0.{Style.RESET_ALL} Cancelar")
            print()
            
            escolha = input("Escolha uma opção: ")
            
            if escolha == "0":
                continue
            
            # Confirmar antes de excluir
            if not confirm_action("Tem certeza que deseja excluir os logs?"):
                print_info("Operação cancelada.")
                pause()
                continue
            
            try:
                data_limite = None
                manter_qtd = None
                
                if escolha == "1":
                    # Manter logs dos últimos 7 dias
                    data_limite = datetime.now() - timedelta(days=7)
                elif escolha == "2":
                    # Manter logs do último mês
                    data_limite = datetime.now() - timedelta(days=30)
                elif escolha == "3":
                    # Manter 10 logs mais recentes
                    manter_qtd = 10
                elif escolha == "4":
                    # Limpar todos
                    data_limite = datetime.now()
                    manter_qtd = 0
                else:
                    print_warning("Opção inválida!")
                    pause()
                    continue
                
                # Processar exclusão
                excluidos = 0
                if manter_qtd is not None:
                    # Excluir com base na quantidade
                    for arquivo in arquivos_log[:-manter_qtd] if manter_qtd > 0 else arquivos_log:
                        os.remove(arquivo)
                        excluidos += 1
                
                elif data_limite is not None:
                    # Excluir com base na data
                    for arquivo in arquivos_log:
                        data_mod = datetime.fromtimestamp(os.path.getmtime(arquivo))
                        if data_mod < data_limite:
                            os.remove(arquivo)
                            excluidos += 1
                
                print_success(f"{excluidos} arquivos de log removidos!")
            
            except Exception as e:
                print_error(f"Erro ao limpar logs: {e}")
                logger.exception("Erro ao limpar logs")
            
            pause()
        
        elif opcao == "0":
            break
        else:
            print_warning("Opção inválida!")
            pause()


def configurar_credenciais():
    """Configura as credenciais das APIs"""
    print_header("CONFIGURAR CREDENCIAIS")
    
    try:
        # Carregar credenciais atuais
        credenciais = {}
        try:
            with open(CONFIG_DIR / "credenciais.json", "r", encoding="utf-8") as f:
                credenciais = json.load(f)
        except FileNotFoundError:
            print_info("Arquivo de credenciais não encontrado. Será criado um novo.")
        except json.JSONDecodeError:
            print_warning("Arquivo de credenciais inválido. Será criado um novo.")
        
        # Mostrar valores atuais
        ow_key = credenciais.get("openweather", {}).get("api_key", "")
        inmet_token = credenciais.get("inmet", {}).get("token", "")
        
        # Solicitar novos valores
        print(f"Chave API OpenWeather atual: {ow_key or '(não configurada)'}")
        nova_ow_key = input("Nova chave API OpenWeather (ENTER para manter atual): ")
        
        print(f"\nToken INMET atual: {inmet_token or '(não configurado)'}")
        novo_inmet_token = input("Novo token INMET (ENTER para manter atual): ")
        
        # Atualizar valores
        if nova_ow_key:
            if "openweather" not in credenciais:
                credenciais["openweather"] = {}
            credenciais["openweather"]["api_key"] = nova_ow_key
        
        if novo_inmet_token:
            if "inmet" not in credenciais:
                credenciais["inmet"] = {}
            credenciais["inmet"]["token"] = novo_inmet_token
        
        # Salvar arquivo
        with open(CONFIG_DIR / "credenciais.json", "w", encoding="utf-8") as f:
            json.dump(credenciais, f, indent=2)
        
        print_success("Credenciais atualizadas com sucesso!")
    
    except Exception as e:
        print_error(f"Erro ao configurar credenciais: {e}")
        logger.exception("Erro ao configurar credenciais")


def menu_configuracoes():
    """Menu de configurações do sistema"""
    while True:
        clear_screen()
        print_header("CONFIGURAÇÕES")
        print(f"{Fore.CYAN}1.{Style.RESET_ALL} Configurar credenciais de API")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} Configurar frequência de coleta")
        print(f"{Fore.CYAN}3.{Style.RESET_ALL} Verificar diretórios do sistema")
        print(f"{Fore.CYAN}0.{Style.RESET_ALL} Voltar")
        print()
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            configurar_credenciais()
            pause()
        
        elif opcao == "2":
            print_header("CONFIGURAR FREQUÊNCIA DE COLETA")
            
            # Aqui você poderia implementar configuração de cron, agendador, etc.
            print_info("Esta funcionalidade configuraria o agendamento da coleta automática.")
            print_info("No Linux/Mac, isso é feito via crontab.")
            print_info("No Windows, via Agendador de Tarefas.")
            
            print("\nExemplo de configuração para crontab:")
            print(f"{Fore.GREEN}# Coleta diária às 2:00 da manhã")
            print(f"0 2 * * * cd {BASE_DIR} && python cli.py coleta atual > /dev/null 2>&1")
            print(f"\n# Coleta histórica semanal (domingo às 3:00)")
            print(f"0 3 * * 0 cd {BASE_DIR} && python cli.py coleta historico > /dev/null 2>&1{Style.RESET_ALL}")
            
            pause()
        
        elif opcao == "3":
            print_header("DIRETÓRIOS DO SISTEMA")
            
            # Verificar diretórios
            diretorios = {
                "Raiz": BASE_DIR,
                "Código-fonte": SRC_DIR,
                "Configuração": CONFIG_DIR,
                "Dados": DADOS_DIR,
                "Logs": LOGS_DIR,
                "Documentação": DOCS_DIR,
                "Temporário": TEMP_DIR
            }
            
            tabela = []
            for nome, diretorio in diretorios.items():
                existe = os.path.exists(diretorio)
                status = f"{Fore.GREEN}OK{Style.RESET_ALL}" if existe else f"{Fore.RED}Não encontrado{Style.RESET_ALL}"
                
                # Verificar permissões
                permissao = "N/A"
                if existe:
                    try:
                        # Testar escrita
                        test_file = os.path.join(diretorio, ".test_write")
                        with open(test_file, "w") as f:
                            f.write("test")
                        os.remove(test_file)
                        permissao = f"{Fore.GREEN}Leitura/Escrita{Style.RESET_ALL}"
                    except PermissionError:
                        permissao = f"{Fore.YELLOW}Somente leitura{Style.RESET_ALL}"
                    except Exception:
                        permissao = f"{Fore.RED}Erro{Style.RESET_ALL}"
                
                tabela.append([nome, str(diretorio), status, permissao])
            
            print_table(tabela, ["Diretório", "Caminho", "Status", "Permissões"])
            
            # Opção para criar diretórios ausentes
            diretorios_ausentes = [d for d, p in diretorios.items() if not os.path.exists(p)]
            if diretorios_ausentes:
                print_warning(f"Diretórios ausentes: {', '.join(diretorios_ausentes)}")
                if confirm_action("Deseja criar os diretórios ausentes?"):
                    for nome in diretorios_ausentes:
                        try:
                            os.makedirs(diretorios[nome], exist_ok=True)
                            print_success(f"Diretório {nome} criado com sucesso!")
                        except Exception as e:
                            print_error(f"Erro ao criar diretório {nome}: {e}")
            
            pause()
        
        elif opcao == "0":
            break
        else:
            print_warning("Opção inválida!")
            pause()


def mostrar_ajuda():
    """Exibe a documentação de ajuda"""
    print_header("AJUDA E DOCUMENTAÇÃO")
    
    # Verificar se a documentação existe
    if (DOCS_DIR / "DOCUMENTACAO.md").exists():
        print_info("Documentação encontrada! Abrindo...")
        
        # Perguntar como deseja visualizar
        print("\nComo deseja visualizar a documentação?")
        print(f"{Fore.CYAN}1.{Style.RESET_ALL} No terminal")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} No navegador (se disponível)")
        print(f"{Fore.CYAN}0.{Style.RESET_ALL} Cancelar")
        print()
        
        escolha = input("Escolha uma opção: ")
        
        if escolha == "1":
            # Mostrar no terminal
            try:
                with open(DOCS_DIR / "DOCUMENTACAO.md", "r", encoding="utf-8") as f:
                    conteudo = f.read()
                
                clear_screen()
                print(conteudo)
            except Exception as e:
                print_error(f"Erro ao ler documentação: {e}")
        
        elif escolha == "2":
            # Abrir no navegador
            try:
                url = "file://" + str(DOCS_DIR / "DOCUMENTACAO.md")
                webbrowser.open(url)
                print_info("Documentação aberta no navegador padrão.")
            except Exception as e:
                print_error(f"Erro ao abrir documentação no navegador: {e}")
    
    else:
        print_warning("Arquivo de documentação não encontrado!")
        print_info("Verifique se o arquivo DOCUMENTACAO.md existe no diretório docs/")
    
    # Mostrar informações básicas
    print("\n=== Sistema de Dados Climáticos ===")
    print("Versão: 1.0.0")
    print("Autor: Equipe de Desenvolvimento")
    print("\nEste sistema permite coletar, analisar e exportar dados climáticos de múltiplas fontes.")
    print("Use o menu principal para navegar entre as funcionalidades.")
    
    print("\n=== Guia Rápido ===")
    print("1. Configure suas regiões em 'Gerenciar Regiões'")
    print("2. Configure as credenciais das APIs em 'Configurações'")
    print("3. Execute a coleta de dados em 'Coleta de Dados'")
    print("4. Visualize os dados em 'Consulta e Análise'")
    print("5. Exporte relatórios em 'Exportação de Dados'")
    
    print("\n=== Contato ===")
    print("Para suporte: suporte@exemplo.com.br")
    print("Para relatar bugs: github.com/usuario/sistema_dados_climaticos/issues")


def coleta_comando(args):
    """Função para executar coleta via linha de comando"""
    try:
        modo = args.modo if hasattr(args, 'modo') else "atual"
        regioes = args.regioes if hasattr(args, 'regioes') else None
        dias = args.dias if hasattr(args, 'dias') else 7
        anos = args.anos if hasattr(args, 'anos') else 15
        
        executar_coleta(modo=modo, regioes=regioes, dias=dias, anos=anos)
        return 0
    except Exception as e:
        print_error(f"Erro na coleta: {e}")
        logger.exception("Erro na coleta via comando")
        return 1


def main():
    """Função principal do CLI"""
    # Verificar se há argumentos de linha de comando
    if len(sys.argv) > 1:
        # Modo de comando (não interativo)
        parser = argparse.ArgumentParser(description="Sistema de Dados Climáticos - CLI")
        subparsers = parser.add_subparsers(dest="comando", help="Comandos disponíveis")
        
        # Comando de coleta
        coleta_parser = subparsers.add_parser("coleta", help="Executar coleta de dados")
        coleta_parser.add_argument("--modo", choices=["atual", "historico", "ambos"], default="atual", help="Modo de coleta")
        coleta_parser.add_argument("--regioes", nargs="+", help="Lista de regiões (opcional)")
        coleta_parser.add_argument("--dias", type=int, default=7, help="Dias para coleta atual")
        coleta_parser.add_argument("--anos", type=int, default=15, help="Anos para coleta histórica")
        
        # Comando de ajuda
        subparsers.add_parser("ajuda", help="Mostrar ajuda do sistema")
        
        # Comando de análise
        analise_parser = subparsers.add_parser("analise", help="Iniciar análise interativa")
        
        args = parser.parse_args()
        
        if args.comando == "coleta":
            return coleta_comando(args)
        elif args.comando == "analise":
            # Iniciar análise interativa
            import subprocess
            subprocess.run([sys.executable, str(SRC_DIR / "exemplo_analise.py")])
            return 0
        elif args.comando == "ajuda":
            mostrar_ajuda()
            return 0
        else:
            parser.print_help()
            return 0
    
    # Modo interativo
    while True:
        opcao = mostrar_menu_principal()
        
        if opcao == "1":
            menu_coleta()
        elif opcao == "2":
            menu_consulta()
        elif opcao == "3":
            menu_regioes()
        elif opcao == "4":
            menu_exportacao()
        elif opcao == "5":
            menu_logs()
        elif opcao == "6":
            menu_configuracoes()
        elif opcao == "7":
            mostrar_ajuda()
            pause()
        elif opcao == "0":
            clear_screen()
            print(f"{Fore.CYAN}Obrigado por usar o Sistema de Dados Climáticos!{Style.RESET_ALL}")
            return 0
        else:
            print_warning("Opção inválida!")
            pause()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nOperação cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print_error(f"Erro inesperado: {e}")
        logger.exception("Erro inesperado na execução do CLI")
        sys.exit(1)