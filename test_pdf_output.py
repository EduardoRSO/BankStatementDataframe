import os
from bank_statement_parser.utils.pdf_extractor import PDFExtractor

def read_passwords(password_file):
    """
    Lê as senhas do arquivo passwords.txt e as separa por vírgulas.
    
    Args:
    - password_file (str): Caminho do arquivo contendo as senhas.
    
    Returns:
    - list: Lista de senhas lidas do arquivo.
    """
    try:
        with open(password_file, "r", encoding="utf-8") as file:
            # Lê o conteúdo e separa as senhas por vírgulas
            passwords = file.read().strip().split(',')
            return [password.strip() for password in passwords]
    except FileNotFoundError:
        print(f"Arquivo de senhas '{password_file}' não encontrado.")
        return []

def test_pdf_extraction_in_extratos():
    """
    Testa a extração de texto de todos os PDFs na pasta 'extratos' e salva os resultados em arquivos .txt.
    """
    extratos_dir = "extratos"
    resultados_dir = "resultados"
    password_file = "passwords.txt"  # Caminho do arquivo com as senhas

    # Lê as senhas do arquivo passwords.txt
    passwords = read_passwords(password_file)

    if not os.path.exists(extratos_dir):
        print(f"Pasta '{extratos_dir}' não encontrada.")
        return

    # Cria a pasta de resultados se não existir
    if not os.path.exists(resultados_dir):
        os.makedirs(resultados_dir)

    # Percorre todos os arquivos na pasta 'extratos'
    for file_name in os.listdir(extratos_dir):
        #if file_name.endswith((".pdf", ".PDF")):
        if file_name.endswith(".PDF"):
            pdf_path = os.path.join(extratos_dir, file_name)
            print(f"\nExtraindo texto do arquivo: {pdf_path}")
            
            # Inicializa o PDFExtractor com as senhas
            pdf_extractor = PDFExtractor(pdf_path, passwords)
            extracted_text = pdf_extractor.extract_text()

            # Salva o texto extraído em um arquivo .txt na pasta 'resultados'
            file_name = file_name.replace(".pdf", ".txt")
            file_name = file_name.replace(".PDF", ".txt")
            output_file_path = os.path.join(resultados_dir, file_name)
            with open(output_file_path, "w", encoding="utf-8") as output_file:
                output_file.write(extracted_text)

            print(f"Texto extraído do PDF '{file_name}' salvo em: {output_file_path}")

if __name__ == "__main__":
    test_pdf_extraction_in_extratos()
