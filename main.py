import os
import sys
import shutil
import unittest
from bank_statement_parser.formats.parser_factory import ParserFactory

def ler_senhas(arquivo_senhas):
    """
    Lê as senhas do arquivo especificado, separando-as por vírgulas.
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
    """
    loader = unittest.TestLoader()
    tests = loader.discover('tests')
    test_runner = unittest.TextTestRunner()
    resultado = test_runner.run(tests)
    return resultado.wasSuccessful()

def processar_arquivos_pdf(pasta_extratos):
    """
    Processa todos os arquivos PDF na pasta indicada, extraindo o texto e salvando
    os resultados em 'transformed_dataframe' dentro da pasta fornecida.
    """
    arquivo_senhas = os.path.join(pasta_extratos, "passwords.txt")
    senhas = ler_senhas(arquivo_senhas)

    # Caminho para o diretório transformed_dataframe dentro da pasta recebida
    pasta_transformada = os.path.join(pasta_extratos, "transformed_dataframe")
    if os.path.exists(pasta_transformada):
        shutil.rmtree(pasta_transformada)
    os.makedirs(pasta_transformada, exist_ok=True)

    # Remove o diretório de resultados anterior, se existir
    pasta_resultados = os.path.join(pasta_extratos, "resultados")
    if os.path.exists(pasta_resultados):
        shutil.rmtree(pasta_resultados)
    os.makedirs(pasta_resultados, exist_ok=True)

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
    if len(sys.argv) < 2:
        print("Uso: python main.py <pasta_dos_arquivos>")
    else:
        pasta_dos_arquivos = sys.argv[1]
        if executar_testes():
            processar_arquivos_pdf(pasta_dos_arquivos)
        else:
            print("Os testes falharam. Corrija os erros antes de continuar.")
