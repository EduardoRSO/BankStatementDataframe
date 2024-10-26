import os
import shutil
import unittest
from bank_statement_parser.formats.parser_factory import ParserFactory

def ler_senhas(arquivo_senhas):
    """
    Lê as senhas do arquivo especificado, separando-as por vírgulas.

    Args:
    - arquivo_senhas (str): Caminho para o arquivo contendo as senhas.

    Retorna:
    - list: Lista de senhas lidas do arquivo.
    """
    try:
        with open(arquivo_senhas, "r", encoding="utf-8") as file:
            senhas = file.read().strip().split(',')
            return [senha.strip() for senha in senhas]
    except FileNotFoundError:
        print(f"Arquivo de senhas '{arquivo_senhas}' não encontrado.")
        return []

def executar_testes():
    """
    Executa todos os testes unitários.
    
    Retorna:
    - bool: True se todos os testes passarem, False caso contrário.
    """
    loader = unittest.TestLoader()
    tests = loader.discover('tests')
    test_runner = unittest.TextTestRunner()
    resultado = test_runner.run(tests)
    return resultado.wasSuccessful()

def processar_arquivos_pdf():
    """
    Processa todos os arquivos PDF na pasta 'extratos', extraindo o texto e salvando
    os resultados em 'transformed_dataframe' para criação de um dashboard no Power BI.
    """
    pasta_extratos = "extratos"
    arquivo_senhas = "passwords.txt"
    senhas = ler_senhas(arquivo_senhas)

    # Remove o diretório 'transformed_dataframe' se ele existir
    pasta_transformada = "transformed_dataframe"
    if os.path.exists(pasta_transformada):
        shutil.rmtree(pasta_transformada)

    if not os.path.exists(pasta_extratos):
        print(f"Pasta '{pasta_extratos}' não encontrada.")
        return

    for nome_arquivo in os.listdir(pasta_extratos):
        if nome_arquivo.endswith((".pdf", ".PDF")):
            caminho_pdf = os.path.join(pasta_extratos, nome_arquivo)
            print(f"\nProcessando arquivo: {caminho_pdf}")

            try:
                parser = ParserFactory.get_parser(caminho_pdf, password_list=senhas)
            except ValueError as e:
                print(f"Erro ao selecionar parser para o arquivo '{nome_arquivo}': {e}")

if __name__ == "__main__":
    if executar_testes():
        processar_arquivos_pdf()
    else:
        print("Os testes falharam. Corrija os erros antes de continuar.")
