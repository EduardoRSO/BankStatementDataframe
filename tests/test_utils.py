import unittest
import os
from bank_statement_parser.utils.pdf_extractor import PDFExtractor

class TestPDFExtractor(unittest.TestCase):

    def setUp(self):
        """
        Método de configuração que é executado antes de cada teste.
        Aqui, criamos um arquivo PDF de teste para ser usado nos testes.
        """
        self.test_pdf_path = "test.pdf"
        self.test_text = "Este é um teste de extração de PDF."

        # Criando um arquivo PDF de teste
        with open(self.test_pdf_path, "w") as f:
            f.write(self.test_text)
        
        self.pdf_extractor = PDFExtractor(self.test_pdf_path)

    def tearDown(self):
        """
        Método de finalização que é executado após cada teste.
        Remove o arquivo PDF de teste criado.
        """
        if os.path.exists(self.test_pdf_path):
            os.remove(self.test_pdf_path)

    def test_extract_text(self):
        """
        Testa se o método 'extract_text()' extrai corretamente o texto do PDF.
        """
        extracted_text = self.pdf_extractor.extract_text()
        self.assertEqual(extracted_text.strip(), self.test_text, "Texto extraído não corresponde ao texto esperado.")

    def test_save_text_to_file(self):
        """
        Testa se o método 'save_text_to_file()' salva corretamente o texto extraído em um arquivo.
        """
        output_path = "output.txt"
        self.pdf_extractor.extract_text()
        self.pdf_extractor.save_text_to_file(output_path)

        # Verifica se o arquivo de saída foi criado
        self.assertTrue(os.path.exists(output_path), "Arquivo de saída não foi criado.")

        # Verifica se o conteúdo do arquivo é o esperado
        with open(output_path, "r") as f:
            saved_text = f.read()
        self.assertEqual(saved_text.strip(), self.test_text, "Texto salvo no arquivo não corresponde ao texto extraído.")

        # Remove o arquivo de saída após o teste
        if os.path.exists(output_path):
            os.remove(output_path)

if __name__ == "__main__":
    unittest.main()
