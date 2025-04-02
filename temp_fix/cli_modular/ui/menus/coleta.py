"""
Menu de coleta de dados meteorológicos.
"""

import logging
import sys
from typing import List, Optional

from .base import SubMenu
from ..console import print_info, print_warning, print_error, print_success, print_header, pause, confirm_action

# Configurar logger
logger = logging.getLogger(__name__)

class MenuColeta(SubMenu):
    """
    Menu para operações de coleta de dados
    """
    
    def __init__(self):
        """Inicializa o menu de coleta"""
        super().__init__("COLETA DE DADOS")
        
        # Adicionar opções do menu
        self.adicionar_item("1", "Coletar dados atuais (últimos 7 dias)", self.coletar_atual)
        self.adicionar_item("2", "Coletar dados históricos", self.coletar_historico)
        self.adicionar_item("3", "Coletar todos os dados (atual + histórico)", self.coletar_ambos)
        self.adicionar_item("4", "Coletar dados para região específica", self.coletar_regiao_especifica)
    
    def coletar_atual(self) -> None:
        """Coleta dados atuais (últimos 7 dias)"""
        print_info("Iniciando coleta de dados atuais...")
        
        try:
            self._executar_coleta(modo="atual")
            print_success("Coleta de dados atuais concluída!")
        except Exception as e:
            print_error(f"Erro ao executar coleta: {e}")
            logger.exception("Erro na coleta de dados atuais")
    
    def coletar_historico(self) -> None:
        """Coleta dados históricos"""
        print_info("Iniciando coleta de dados históricos...")
        
        # Confirmar ação devido ao tempo que pode levar
        if not confirm_action("A coleta de dados históricos pode levar muito tempo. Deseja continuar?"):
            print_info("Operação cancelada pelo usuário")
            return
        
        try:
            self._executar_coleta(modo="historico")
            print_success("Coleta de dados históricos concluída!")
        except Exception as e:
            print_error(f"Erro ao executar coleta: {e}")
            logger.exception("Erro na coleta de dados históricos")
    
    def coletar_ambos(self) -> None:
        """Coleta dados atuais e históricos"""
        print_info("Iniciando coleta completa de dados...")
        
        # Confirmar ação devido ao tempo que pode levar
        if not confirm_action("A coleta completa de dados pode levar muito tempo. Deseja continuar?"):
            print_info("Operação cancelada pelo usuário")
            return
        
        try:
            self._executar_coleta(modo="ambos")
            print_success("Coleta completa de dados concluída!")
        except Exception as e:
            print_error(f"Erro ao executar coleta: {e}")
            logger.exception("Erro na coleta completa de dados")
    
    def coletar_regiao_especifica(self) -> None:
        """Coleta dados para uma região específica"""
        from ...core.config import config
        
        # Obter lista de regiões disponíveis
        regioes = config.get_regioes()
        
        if not regioes:
            print_warning("Nenhuma região configurada encontrada!")
            return
        
        print_header("REGIÕES DISPONÍVEIS")
        for i, regiao in enumerate(regioes, 1):
            print(f"{i}. {regiao['nome']} - {regiao['descricao']}")
        print()
        
        try:
            escolha = input("Escolha uma região (número) ou ENTER para todas: ").strip()
            regiao_escolhida = None
            
            if escolha:
                indice = int(escolha) - 1
                if 0 <= indice < len(regioes):
                    regiao_escolhida = [regioes[indice]["nome"]]
                    print_info(f"Região selecionada: {regiao_escolhida[0]}")
                else:
                    print_error("Índice inválido!")
                    return
            
            # Escolher tipo de dados
            print("\nTipo de dados:")
            print("1. Dados atuais (últimos dias)")
            print("2. Dados históricos (anos anteriores)")
            print("3. Ambos (atual + histórico)")
            
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
            
            # Executar coleta
            print_info(f"Iniciando coleta no modo {modo}...")
            self._executar_coleta(modo=modo, regioes=regiao_escolhida)
            print_success("Coleta concluída!")
            
        except ValueError:
            print_error("Entrada inválida!")
        except Exception as e:
            print_error(f"Erro ao executar coleta: {e}")
            logger.exception("Erro na coleta para região específica")
    
    def _executar_coleta(self, modo: str, regioes: Optional[List[str]] = None, 
                         dias: int = 7, anos: int = 15) -> None:
        """
        Executa a coleta de dados
        
        Args:
            modo: 'atual', 'historico' ou 'ambos'
            regioes: Lista opcional de nomes de regiões
            dias: Número de dias para dados atuais
            anos: Número de anos para dados históricos
        """
        # Importar o módulo necessário
        sys.path.append(str(self._get_src_dir()))
        from src.executar_coleta import main as executar_coleta_main
        
        # Preparar argumentos
        cmd_args = ["--modo", modo]
        
        if regioes:
            cmd_args.extend(["--regioes"] + regioes)
        if dias != 7:
            cmd_args.extend(["--dias", str(dias)])
        if anos != 15:
            cmd_args.extend(["--anos", str(anos)])
        
        # Salvar argumentos originais
        original_args = sys.argv.copy()
        
        try:
            # Substituir sys.argv com nossos argumentos e executar
            sys.argv = [sys.argv[0]] + cmd_args
            print_info(f"Executando coleta com argumentos: {' '.join(cmd_args)}")
            executar_coleta_main()
        finally:
            # Restaurar argumentos originais
            sys.argv = original_args
    
    def _get_src_dir(self):
        """Obtém o diretório src do projeto"""
        from pathlib import Path
        return Path(__file__).parent.parent.parent.parent.parent / "src"