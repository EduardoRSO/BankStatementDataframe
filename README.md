# BankStatementParser

**BankStatementParser** é uma ferramenta em Python projetada para extrair dados de extratos bancários em formato PDF e convertê-los em um DataFrame. Esse DataFrame pode ser utilizado para gerar dashboards e facilitar a análise financeira de maneira automatizada.

## Funcionalidades

- Suporte para extratos bancários dos seguintes formatos:
  - Caixa
  - Bradesco
  - Carrefour
  - Itaú
- Extração de dados dos PDFs de forma eficiente.
- Limpeza e tratamento dos dados extraídos para garantir consistência.
- Processamento dos dados em um DataFrame pronto para ser integrado em dashboards.
- Suporte para testes unitários.

## Estrutura do Projeto

```bash
BankStatementParser/
│
├── README.md                # Descrição geral do projeto
├── requirements.txt          # Lista de dependências
├── setup.py                  # Script para instalação do pacote
├── .gitignore                # Arquivos e pastas para ignorar no Git
│
├── bank_statement_parser/    # Diretório principal do projeto
│   ├── __init__.py           # Inicialização do módulo Python
│   ├── parser.py             # Módulo principal para parsing de PDFs
│   ├── formats/              # Diretório contendo as classes para diferentes formatos de extratos
│   │   ├── __init__.py
│   │   ├── caixa.py          # Parser específico para o formato de extrato da Caixa
│   │   ├── bradesco.py       # Parser específico para o formato de extrato do Bradesco
│   │   ├── carrefour.py      # Parser específico para o formato de extrato do Carrefour
│   │   └── itau.py           # Parser específico para o formato de extrato do Itaú
│   │
│   └── utils/                # Diretório para utilidades de extração, limpeza e processamento
│       ├── __init__.py
│       ├── pdf_extractor.py  # Funções para extração de dados dos PDFs
│       ├── data_cleaner.py   # Funções para limpeza e tratamento dos dados extraídos
│       └── dataframe_processor.py  # Funções para processamento e geração do DataFrame final
│
└── tests/                    # Diretório para os testes unitários
    ├── __init__.py
    ├── test_parser.py        # Testes para o parser principal
    └── test_utils.py         # Testes para as utilidades (extração, limpeza, processamento)
```

