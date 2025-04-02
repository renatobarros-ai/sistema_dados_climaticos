#!/usr/bin/env python3
"""
Script para execução da coleta de dados climáticos.
Este script é ideal para uso via linha de comando ou agendador (cron).
"""

import argparse
import sys
import logging
from datetime import datetime
from pathlib import Path
from coletor_climatico import ColetorDadosClimaticos

# Configurar logger para este script
DIRETORIO_BASE = Path(__file__).parent.parent
DIRETORIO_LOGS = DIRETORIO_BASE / "logs"

# Organizar logs por ano/mês, semelhante aos dados
hoje = datetime.now()
diretorio_log_ano = DIRETORIO_LOGS / str(hoje.year)
diretorio_log_mes = diretorio_log_ano / f"{hoje.month:02d}"

# Criar diretórios de log se não existirem
diretorio_log_ano.mkdir(exist_ok=True, parents=True)
diretorio_log_mes.mkdir(exist_ok=True, parents=True)

arquivo_log = diretorio_log_mes / f"execucao_{hoje.strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(arquivo_log),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Função principal para execução da coleta"""
    parser = argparse.ArgumentParser(description="Execução de Coleta de Dados Climáticos")
    parser.add_argument('--modo', choices=['atual', 'historico', 'ambos'], 
                        default='atual', help='Modo de coleta de dados')
    parser.add_argument('--regioes', nargs='+', help='Lista de regiões específicas (opcional)')
    parser.add_argument('--dias', type=int, default=7, 
                        help='Número de dias para coleta de dados atuais (1-30)')
    parser.add_argument('--anos', type=int, default=15, 
                        help='Número de anos para coleta de dados históricos (1-30)')
    
    args = parser.parse_args()
    
    # Validação de parâmetros
    if args.dias < 1 or args.dias > 30:
        logger.error("O número de dias deve estar entre 1 e 30")
        return 1
    
    if args.anos < 1 or args.anos > 30:
        logger.error("O número de anos deve estar entre 1 e 30")
        return 1
    
    logger.info(f"Iniciando execução no modo: {args.modo}")
    logger.info(f"Configurações: dias={args.dias}, anos={args.anos}")
    
    if args.regioes:
        logger.info(f"Regiões específicas: {', '.join(args.regioes)}")
    
    try:
        # Inicializar o coletor
        coletor = ColetorDadosClimaticos()
        
        # Executar coleta conforme modo
        if args.modo in ('atual', 'ambos'):
            logger.info("Iniciando coleta de dados atuais")
            coletor.coletar_para_todas_regioes(modo="atual", regioes_especificas=args.regioes)
            logger.info("Coleta de dados atuais finalizada")
        
        if args.modo in ('historico', 'ambos'):
            logger.info("Iniciando coleta de dados históricos")
            coletor.coletar_para_todas_regioes(modo="historico", regioes_especificas=args.regioes)
            logger.info("Coleta de dados históricos finalizada")
        
        logger.info("Execução concluída com sucesso")
        return 0
        
    except Exception as e:
        logger.error(f"Erro durante a execução: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())