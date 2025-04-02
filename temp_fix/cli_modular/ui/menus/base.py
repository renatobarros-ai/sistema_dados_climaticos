"""
Menu base para o sistema de menus do CLI.
Define a estrutura e comportamento padrão de todos os menus.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Callable, Optional, Any, TypeVar, Generic
from colorama import Fore, Style

from ..console import clear_screen, print_header, pause, print_warning

# Tipo genérico para o resultado de callbacks de menu
T = TypeVar('T')

class MenuItem(Generic[T]):
    """
    Representa um item de menu com identificador, texto e função de callback
    
    Attributes:
        id (str): Identificador do item no menu
        texto (str): Texto a ser exibido
        callback (Callable[[], Optional[T]]): Função a ser chamada quando o item for selecionado
    """
    def __init__(self, id: str, texto: str, callback: Callable[[], Optional[T]]):
        self.id = id
        self.texto = texto
        self.callback = callback
        
    def executar(self) -> Optional[T]:
        """Executa o callback do item de menu"""
        return self.callback()

class Menu(ABC, Generic[T]):
    """
    Classe base para todos os menus do sistema
    
    Attributes:
        titulo (str): Título do menu
        itens (List[MenuItem]): Lista de itens do menu
        opcao_voltar (MenuItem): Item para voltar ao menu anterior
    """
    def __init__(self, titulo: str):
        self.titulo = titulo
        self.itens: List[MenuItem[T]] = []
        self.opcao_voltar = MenuItem("0", "Voltar", lambda: None)
    
    def adicionar_item(self, id: str, texto: str, callback: Callable[[], Optional[T]]) -> None:
        """
        Adiciona um item ao menu
        
        Args:
            id: Identificador do item
            texto: Texto a ser exibido
            callback: Função a ser chamada quando o item for selecionado
        """
        self.itens.append(MenuItem(id, texto, callback))
    
    def exibir(self) -> None:
        """Exibe o menu e processa a escolha do usuário"""
        while True:
            clear_screen()
            print_header(self.titulo)
            
            # Exibir itens do menu
            for item in self.itens:
                self._renderizar_item(item)
            
            # Exibir opção de voltar
            self._renderizar_item(self.opcao_voltar)
            print()
            
            # Capturar escolha do usuário
            escolha = input("Escolha uma opção: ")
            
            # Processar escolha
            if escolha == self.opcao_voltar.id:
                return
            
            # Procurar e executar o item correspondente
            for item in self.itens:
                if item.id == escolha:
                    resultado = item.executar()
                    if resultado is not None:
                        pause()
                    break
            else:
                print_warning("Opção inválida!")
                pause()
    
    def _renderizar_item(self, item: MenuItem[T]) -> None:
        """
        Renderiza um item do menu no console
        
        Args:
            item: O item a ser renderizado
        """
        print(f"{Fore.CYAN}{item.id}.{Style.RESET_ALL} {item.texto}")


class SubMenu(Menu[T]):
    """Menu que será exibido como um submenu de outro menu"""
    
    def como_callback(self) -> Callable[[], None]:
        """
        Retorna uma função que pode ser usada como callback de um item de menu
        
        Returns:
            Callable: Função para exibir este menu
        """
        return self.exibir