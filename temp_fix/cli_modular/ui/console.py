"""
Funções para interface de console do Sistema de Dados Climáticos.
Centraliza formatação, exibição e entrada de dados no terminal.
"""

import os
from typing import List, Dict, Any, Optional
from colorama import init, Fore, Style
from tabulate import tabulate

# Inicializar colorama para cores no terminal
init(autoreset=True)

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

def clear_screen() -> None:
    """Limpa a tela do terminal de forma compatível com diferentes sistemas"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(texto: str) -> None:
    """
    Imprime um cabeçalho formatado na tela
    
    Args:
        texto: O texto a ser exibido como cabeçalho
    """
    largura = 70
    print("\n" + "=" * largura)
    print(f"{Fore.CYAN}{texto.center(largura)}{Style.RESET_ALL}")
    print("=" * largura + "\n")

def print_info(texto: str) -> None:
    """
    Imprime informação formatada na tela
    
    Args:
        texto: A mensagem informativa
    """
    print(f"{Fore.GREEN}ℹ {texto}{Style.RESET_ALL}")

def print_warning(texto: str) -> None:
    """
    Imprime aviso formatado na tela
    
    Args:
        texto: A mensagem de aviso
    """
    print(f"{Fore.YELLOW}⚠ {texto}{Style.RESET_ALL}")

def print_error(texto: str) -> None:
    """
    Imprime erro formatado na tela
    
    Args:
        texto: A mensagem de erro
    """
    print(f"{Fore.RED}✖ {texto}{Style.RESET_ALL}")

def print_success(texto: str) -> None:
    """
    Imprime mensagem de sucesso formatada na tela
    
    Args:
        texto: A mensagem de sucesso
    """
    print(f"{Fore.GREEN}✓ {texto}{Style.RESET_ALL}")

def print_table(data: List[Any], headers: List[str]) -> None:
    """
    Imprime uma tabela formatada na tela
    
    Args:
        data: Os dados da tabela
        headers: Os cabeçalhos da tabela
    """
    print(tabulate(data, headers=headers, tablefmt="grid"))

def pause() -> None:
    """Pausa a execução até o usuário pressionar ENTER"""
    input(f"\n{Fore.YELLOW}Pressione ENTER para continuar...{Style.RESET_ALL}")

def confirm_action(mensagem: str = "Confirma esta ação?") -> bool:
    """
    Solicita confirmação do usuário para uma ação
    
    Args:
        mensagem: A mensagem de confirmação
        
    Returns:
        bool: True se o usuário confirmou, False caso contrário
    """
    resposta = input(f"{Fore.YELLOW}{mensagem} (s/n): {Style.RESET_ALL}").lower()
    return resposta in ['s', 'sim', 'y', 'yes']

def get_option(prompt: str, options: List[str], default: Optional[int] = None) -> int:
    """
    Solicita que o usuário escolha uma opção de uma lista
    
    Args:
        prompt: A mensagem de solicitação
        options: A lista de opções
        default: O índice da opção padrão (se houver)
        
    Returns:
        int: O índice da opção escolhida
    """
    # Exibir as opções
    for i, opcao in enumerate(options, 1):
        print(f"{Fore.CYAN}{i}.{Style.RESET_ALL} {opcao}")
    
    # Preparar mensagem com valor padrão, se existir
    if default is not None:
        prompt_completo = f"\n{prompt} [{default+1}]: "
    else:
        prompt_completo = f"\n{prompt}: "
    
    # Solicitar entrada
    while True:
        try:
            entrada = input(prompt_completo)
            
            # Usar o valor padrão se a entrada for vazia
            if entrada.strip() == "" and default is not None:
                return default
            
            # Converter para inteiro e validar
            escolha = int(entrada)
            if 1 <= escolha <= len(options):
                return escolha - 1
            else:
                print_warning(f"Opção inválida. Escolha um número entre 1 e {len(options)}.")
        except ValueError:
            print_warning("Entrada inválida. Digite um número.")

def get_input(prompt: str, default: Optional[str] = None) -> str:
    """
    Solicita texto ao usuário com valor padrão opcional
    
    Args:
        prompt: A mensagem de solicitação
        default: O valor padrão (se houver)
        
    Returns:
        str: O texto informado pelo usuário ou o valor padrão
    """
    if default:
        resposta = input(f"{prompt} [{default}]: ").strip()
        return resposta if resposta else default
    else:
        return input(f"{prompt}: ").strip()

def display_menu(title: str, options: Dict[str, str]) -> str:
    """
    Exibe um menu e retorna a opção escolhida pelo usuário
    
    Args:
        title: O título do menu
        options: Dicionário com ids e textos das opções
        
    Returns:
        str: O id da opção escolhida
    """
    clear_screen()
    print_header(title)
    
    # Exibir as opções
    for id_opcao, texto_opcao in options.items():
        print(f"{Fore.CYAN}{id_opcao}.{Style.RESET_ALL} {texto_opcao}")
    
    print()
    return input("Escolha uma opção: ")

def show_banner() -> None:
    """Exibe o banner do sistema"""
    print(BANNER)