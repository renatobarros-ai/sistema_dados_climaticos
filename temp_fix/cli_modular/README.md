# CLI Modular - Sistema de Dados Climáticos

Esta é uma versão modular e refatorada do CLI original do Sistema de Dados Climáticos.

## Estrutura

```
cli_modular/
├── __init__.py               # Módulo principal
├── main.py                   # Ponto de entrada
├── ui/                       # Interface de usuário
│   ├── __init__.py
│   ├── console.py            # Funções de console (print, formatação)
│   ├── menus/                # Definições de menus
│       ├── __init__.py
│       ├── base.py           # Classes base de menu
│       ├── principal.py      # Menu principal
│       ├── coleta.py         # Menu de coleta de dados
│       └── ...               # Outros menus
├── core/                     # Lógica de negócio
│   ├── __init__.py
│   ├── config.py             # Gerenciamento de configuração
│   └── ...                   # Outros componentes core
└── utils/                    # Utilitários
    ├── __init__.py
    └── ...                   # Funcionalidades auxiliares
```

## Benefícios da Refatoração

1. **Manutenibilidade**: Código organizado em módulos coesos e com responsabilidades bem definidas
2. **Testabilidade**: Separação clara entre UI e lógica facilita testes
3. **Reutilização**: Componentes compartilhados (como UI de console) são implementados uma vez
4. **Extensibilidade**: Novos menus ou funcionalidades podem ser adicionados facilmente
5. **Legibilidade**: Arquivos menores e mais focados são mais fáceis de entender

## Como Usar

A nova versão mantém a mesma interface de usuário e funcionalidades do CLI original, mas com melhor organização interna.

```bash
# Modo interativo
python main.py

# Modo de comando
python main.py coleta --modo atual
python main.py analise
python main.py ajuda
```

## Implementação

A implementação atual inclui exemplos de:

- **Classe base de Menu**: Modelo para todos os menus do sistema
- **Sistema de Configuração**: Gerencia configurações centralizadas 
- **UI de Console**: Funções para interface no terminal
- **Menu Principal e de Coleta**: Exemplos completos de menus

Para uma implementação completa, seria necessário criar todos os menus e funcionalidades do sistema original.