import os
from bank_statement_parser.utils.pdf_extractor import PDFExtractor

def test_pdf_extraction_in_extratos():
    """
    Testa a extração de texto de todos os PDFs na pasta 'extratos' e salva os resultados em arquivos .txt.
    """
    extratos_dir = "extratos"
    resultados_dir = "resultados"

    if not os.path.exists(extratos_dir):
        print(f"Pasta '{extratos_dir}' não encontrada.")
        return

    # Cria a pasta de resultados se não existir
    if not os.path.exists(resultados_dir):
        os.makedirs(resultados_dir)

    # Percorre todos os arquivos na pasta 'extratos'
    for file_name in os.listdir(extratos_dir):
        if file_name.endswith(".pdf"):
            pdf_path = os.path.join(extratos_dir, file_name)
            print(f"\nExtraindo texto do arquivo: {pdf_path}")
            
            # Inicializa o PDFExtractor
            pdf_extractor = PDFExtractor(pdf_path)
            extracted_text = pdf_extractor.extract_text()

            # Salva o texto extraído em um arquivo .txt na pasta 'resultados'
            output_file_path = os.path.join(resultados_dir, file_name.replace(".pdf", ".txt"))
            with open(output_file_path, "w", encoding="utf-8") as output_file:
                output_file.write(extracted_text)

            print(f"Texto extraído do PDF '{file_name}' salvo em: {output_file_path}")

if __name__ == "__main__":
    test_pdf_extraction_in_extratos()
