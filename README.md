BankStatementParser
BankStatementParser é uma ferramenta em Python projetada para processar extratos bancários em PDF, extraindo e classificando dados transacionais. Esses dados são convertidos para um DataFrame, permitindo integração com Power BI para análise financeira.

Funcionalidades
Suporte para os seguintes bancos:
Caixa, Bradesco, Carrefour, Itaú e Inter
Classificação das transações em Receitas e Custos, com categorias específicas para cada banco.
Extração, limpeza e transformação dos dados, com geração de arquivos prontos para visualização.
Carregamento dinâmico de categorias a partir de um arquivo Excel externo (categorias_definicoes.xlsx).
Testes unitários para verificação de funcionalidades essenciais.
Configuração do Power BI
O projeto não inclui o arquivo do Power BI, mas você pode configurar uma Visualização de Matriz com a seguinte hierarquia para análise dos dados:

Hierarquia: tipo > categoria > origem > descricao
Campo de valor: net, representando o saldo de transações
Essa visualização permite explorar as transações de forma hierárquica, facilitando a análise de receitas e despesas.

Requisitos e Configuração do Ambiente
Estrutura de Pastas
O projeto espera uma pasta contendo:

Arquivos PDF dos extratos bancários a serem processados.
Um arquivo passwords.txt com senhas para desbloqueio dos PDFs, se necessário.
O arquivo categorias_definicoes.xlsx, que contém as definições de categorias para cada banco.
Esses arquivos devem estar no diretório especificado ao rodar o script.

Criação e Ativação do Ambiente Virtual
Para configurar o ambiente:

Crie e ative um ambiente virtual:

bash
Copiar código
python -m venv venv

Ative o ambiente
No Windows
venv\Scripts\activate
No macOS/Linux
source venv/bin/activate
Instale as dependências listadas no requirements.txt:

bash
Copiar código
pip install -r requirements.txt
Como Executar
Para processar os arquivos PDF, execute o seguinte comando, passando o diretório onde estão os arquivos:

bash
Copiar código
python main.py <caminho_para_a_pasta>
Nota: O <caminho_para_a_pasta> deve incluir o passwords.txt e o categorias_definicoes.xlsx.

Estrutura do Projeto
bash
Copiar código
BankStatementParser/
│
├── README.md                   # Descrição do projeto
├── requirements.txt            # Dependências do projeto
├── setup.py                    # Script de instalação
├── .gitignore                  # Arquivos ignorados pelo Git
│
├── bank_statement_parser/      # Diretório principal do projeto
│   ├── __init__.py             
│   ├── formats/                # Parsers específicos para cada banco
│   │   ├── caixa.py            
│   │   ├── bradesco.py         
│   │   ├── carrefour.py        
│   │   ├── itau.py             
│   │   └── inter.py            
│   │
│   └── utils/                  # Ferramentas de extração e processamento
│       ├── pdf_extractor.py    # Funções para extração de PDFs
│       └── data_cleaner.py     # Funções de limpeza de dados
│
└── tests/                      # Testes unitários
    ├── test_parser.py          
    └── test_utils.py           
Com essas instruções, você pode configurar e executar o projeto para automatizar a análise dos extratos bancários em PDF.