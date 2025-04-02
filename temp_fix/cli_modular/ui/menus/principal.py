"""
Menu principal do Sistema de Dados Climáticos.
Ponto de entrada para todas as funcionalidades.
"""

from typing import Dict

from .base import Menu, SubMenu
from ..console import show_banner
from .coleta import MenuColeta
from .analise import MenuAnalise
from .regioes import MenuRegioes
from .exportacao import MenuExportacao
from .logs import MenuLogs
from .config import MenuConfiguracao

class MenuPrincipal(Menu):
    """
    Menu principal do sistema
    """
    
    def __init__(self):
        """Inicializa o menu principal"""
        super().__init__("MENU PRINCIPAL")
        
        # Inicializar submenus
        self.menu_coleta = MenuColeta()
        self.menu_analise = MenuAnalise()
        self.menu_regioes = MenuRegioes()
        self.menu_exportacao = MenuExportacao()
        self.menu_logs = MenuLogs()
        self.menu_configuracao = MenuConfiguracao()
        
        # Adicionar itens de menu
        self.adicionar_item("1", "Coleta de Dados", self.menu_coleta.como_callback())
        self.adicionar_item("2", "Consulta e Análise", self.menu_analise.como_callback())
        self.adicionar_item("3", "Gerenciar Regiões", self.menu_regioes.como_callback())
        self.adicionar_item("4", "Exportação de Dados", self.menu_exportacao.como_callback())
        self.adicionar_item("5", "Logs e Monitoramento", self.menu_logs.como_callback())
        self.adicionar_item("6", "Configurações", self.menu_configuracao.como_callback())
        self.adicionar_item("7", "Ajuda e Documentação", self.mostrar_ajuda)
        
        # Customizar opção de saída
        self.opcao_voltar.id = "0"
        self.opcao_voltar.texto = "Sair"
    
    def exibir(self) -> None:
        """Exibe o menu principal com o banner"""
        from ..console import clear_screen, print_header
        
        while True:
            clear_screen()
            show_banner()
            print_header(self.titulo)
            
            # Exibir itens do menu
            for item in self.itens:
                self._renderizar_item(item)
            
            # Exibir opção de sair
            self._renderizar_item(self.opcao_voltar)
            print()
            
            # Capturar escolha do usuário
            escolha = input("Escolha uma opção: ")
            
            # Processar escolha
            if escolha == self.opcao_voltar.id:
                from ..console import clear_screen, Fore, Style
                clear_screen()
                print(f"{Fore.CYAN}Obrigado por usar o Sistema de Dados Climáticos!{Style.RESET_ALL}")
                return
            
            # Procurar e executar o item correspondente
            for item in self.itens:
                if item.id == escolha:
                    item.executar()
                    break
            else:
                from ..console import print_warning, pause
                print_warning("Opção inválida!")
                pause()
    
    def mostrar_ajuda(self) -> None:
        """Exibe a ajuda do sistema"""
        from pathlib import Path
        from ..console import clear_screen, print_header, print_info, print_warning, pause
        import os
        import webbrowser
        
        # Verificar se a documentação existe
        docs_dir = Path(__file__).parent.parent.parent.parent.parent / "docs"
        doc_file = docs_dir / "DOCUMENTACAO.md"
        
        clear_screen()
        print_header("AJUDA E DOCUMENTAÇÃO")
        
        if doc_file.exists():
            print_info("Documentação encontrada!")
            
            # Perguntar como deseja visualizar
            print("\nComo deseja visualizar a documentação?")
            print("1. No terminal")
            print("2. No navegador (se disponível)")
            print("0. Cancelar")
            print()
            
            escolha = input("Escolha uma opção: ")
            
            if escolha == "1":
                # Mostrar no terminal
                try:
                    with open(doc_file, "r", encoding="utf-8") as f:
                        conteudo = f.read()
                    
                    clear_screen()
                    print(conteudo)
                except Exception as e:
                    print_warning(f"Erro ao ler documentação: {e}")
            
            elif escolha == "2":
                # Abrir no navegador
                try:
                    url = "file://" + str(doc_file)
                    webbrowser.open(url)
                    print_info("Documentação aberta no navegador padrão.")
                except Exception as e:
                    print_warning(f"Erro ao abrir documentação no navegador: {e}")
        
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
        
        pause()