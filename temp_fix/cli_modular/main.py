#!/usr/bin/env python3
"""
Ponto de entrada principal para o CLI do Sistema de Dados Climáticos.
"""

import sys
import logging
import argparse
from pathlib import Path
from datetime import datetime
import traceback

# Configurar logging
def configurar_logging():
    """Configura o logging do sistema"""
    from core.config import config
    
    # Obter diretório de logs para data atual
    diretorio_log = config.get_log_dir_for_current_date()
    
    # Nome do arquivo de log
    hoje = datetime.now()
    arquivo_log = diretorio_log / f"cli_{hoje.strftime('%Y%m%d')}.log"
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(arquivo_log),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Criar logger específico
    return logging.getLogger("cli")

# Função principal em modo interativo
def modo_interativo():
    """Inicia o CLI em modo interativo"""
    from ui.menus.principal import MenuPrincipal
    
    # Criar e exibir menu principal
    menu = MenuPrincipal()
    menu.exibir()
    
    return 0

# Função para executar coleta via comando
def executar_coleta(args):
    """Executa a coleta de dados via comando"""
    logger.info(f"Executando coleta via comando: {args}")
    
    try:
        # Adicionar diretório src ao path
        src_dir = Path(__file__).parent.parent / "src"
        sys.path.append(str(src_dir))
        
        # Importar módulo de execução
        from src.executar_coleta import main as executar_coleta_main
        
        # Executar módulo
        return executar_coleta_main()
    except Exception as e:
        logger.error(f"Erro na coleta: {e}")
        from ui.console import print_error
        print_error(f"Erro na coleta: {e}")
        return 1

# Função para executar análise interativa
def executar_analise():
    """Executa a análise interativa de dados"""
    logger.info("Executando análise interativa")
    
    try:
        # Adicionar diretório src ao path
        src_dir = Path(__file__).parent.parent / "src"
        sys.path.append(str(src_dir))
        
        # Importar e executar módulo
        import subprocess
        resultado = subprocess.run([sys.executable, str(src_dir / "exemplo_analise.py")])
        return resultado.returncode
    except Exception as e:
        logger.error(f"Erro na análise: {e}")
        from ui.console import print_error
        print_error(f"Erro na análise: {e}")
        return 1

# Função principal
def main():
    """Função principal do CLI"""
    global logger
    logger = configurar_logging()
    
    # Verificar se há argumentos de linha de comando
    if len(sys.argv) > 1:
        # Modo de comando (não interativo)
        parser = argparse.ArgumentParser(description="Sistema de Dados Climáticos - CLI")
        subparsers = parser.add_subparsers(dest="comando", help="Comandos disponíveis")
        
        # Comando de coleta
        coleta_parser = subparsers.add_parser("coleta", help="Executar coleta de dados")
        coleta_parser.add_argument("--modo", choices=["atual", "historico", "ambos"], default="atual", 
                                 help="Modo de coleta")
        coleta_parser.add_argument("--regioes", nargs="+", help="Lista de regiões (opcional)")
        coleta_parser.add_argument("--dias", type=int, default=7, help="Dias para coleta atual")
        coleta_parser.add_argument("--anos", type=int, default=15, help="Anos para coleta histórica")
        
        # Comando de ajuda
        subparsers.add_parser("ajuda", help="Mostrar ajuda do sistema")
        
        # Comando de análise
        subparsers.add_parser("analise", help="Iniciar análise interativa")
        
        args = parser.parse_args()
        
        if args.comando == "coleta":
            return executar_coleta(args)
        elif args.comando == "analise":
            return executar_analise()
        elif args.comando == "ajuda":
            from ui.menus.principal import MenuPrincipal
            menu = MenuPrincipal()
            menu.mostrar_ajuda()
            return 0
        else:
            parser.print_help()
            return 0
    
    # Modo interativo
    return modo_interativo()

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nOperação cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro inesperado: {e}")
        traceback.print_exc()
        logging.getLogger("cli").exception("Erro inesperado na execução do CLI")
        sys.exit(1)