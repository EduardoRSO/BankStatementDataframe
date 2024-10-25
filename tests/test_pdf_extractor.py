import unittest
import os
import logging
from PyPDF2 import PdfWriter
from bank_statement_parser.utils.pdf_extractor import PDFExtractor
from reportlab.pdfgen import canvas

class TestPDFExtractor(unittest.TestCase):

    def setUp(self):
        """
        Método de configuração que é executado antes de cada teste.
        Aqui, criamos um arquivo PDF de teste válido usando reportlab.
        """
        # Configurando o logger
        self.logger = logging.getLogger("TestPDFExtractor")
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

        self.test_pdf_path = "test.pdf"
        self.test_text = "Este é um teste de extração de PDF."

        # Criando um arquivo PDF válido de teste usando reportlab
        self.logger.debug(f"Criando arquivo PDF de teste válido em: {self.test_pdf_path}")
        self.create_test_pdf(self.test_pdf_path, self.test_text)
        
        self.logger.debug(f"Instanciando PDFExtractor para o caminho: {self.test_pdf_path}")
        self.pdf_extractor = PDFExtractor(self.test_pdf_path)

    def tearDown(self):
        """
        Método de finalização que é executado após cada teste.
        Remove o arquivo PDF de teste criado.
        """
        if os.path.exists(self.test_pdf_path):
            self.logger.debug(f"Removendo arquivo de teste: {self.test_pdf_path}")
            os.remove(self.test_pdf_path)

    def create_test_pdf(self, path, text):
        """
        Cria um arquivo PDF válido com o texto fornecido.

        Args:
        - path (str): Caminho do arquivo PDF.
        - text (str): Texto que será adicionado ao PDF.
        """
        c = canvas.Canvas(path)
        c.drawString(100, 750, text)  # Adiciona o texto na posição especificada
        c.save()

    def test_extract_text(self):
        """
        Testa se o método 'extract_text()' extrai corretamente o texto do PDF.
        """
        self.logger.debug(f"Extraindo texto do PDF: {self.test_pdf_path}")
        extracted_text = self.pdf_extractor.extract_text()
        self.logger.debug(f"Texto extraído: {extracted_text}")
        self.assertEqual(extracted_text.strip(), self.test_text, "Texto extraído não corresponde ao texto esperado.")

    def test_save_text_to_file(self):
        """
        Testa se o método 'save_text_to_file()' salva corretamente o texto extraído em um arquivo.
        """
        output_path = "output.txt"
        self.logger.debug(f"Extraindo texto e salvando em: {output_path}")
        self.pdf_extractor.extract_text()
        self.pdf_extractor.save_text_to_file(output_path)

        # Verifica se o arquivo de saída foi criado
        file_exists = os.path.exists(output_path)
        self.logger.debug(f"Arquivo de saída criado: {file_exists}")
        self.assertTrue(file_exists, "Arquivo de saída não foi criado.")

        # Verifica se o conteúdo do arquivo é o esperado (lendo o arquivo com UTF-8)
        if file_exists:
            with open(output_path, "r", encoding="utf-8") as f:
                saved_text = f.read()
            self.logger.debug(f"Conteúdo salvo: {saved_text}")
            self.assertEqual(saved_text.strip(), self.test_text, "Texto salvo no arquivo não corresponde ao texto extraído.")

            # Remove o arquivo de saída após o teste
            if os.path.exists(output_path):
                self.logger.debug(f"Removendo arquivo de saída: {output_path}")
                os.remove(output_path)

    def test_pdf_extractor_with_password(self):
        """
        Testa se o PDFExtractor consegue extrair o texto de um PDF protegido com a senha correta.
        """
        protected_pdf_path = "test_password_protected.pdf"
        test_password = "12345"
        
        # Cria um PDF protegido por senha
        writer = PdfWriter()
        writer.add_page(writer.add_blank_page(width=595.28, height=841.89))
        writer.encrypt(test_password)
        with open(protected_pdf_path, "wb") as f:
            writer.write(f)

        # Testa a extração de texto com a senha correta
        pdf_extractor = PDFExtractor(protected_pdf_path, password_list=[test_password])
        extracted_text = pdf_extractor.extract_text()
        self.assertIsInstance(extracted_text, str)  # Certifica-se de que algum texto é retornado

        # Remove o arquivo protegido por senha após o teste
        if os.path.exists(protected_pdf_path):
            os.remove(protected_pdf_path)

if __name__ == "__main__":
    unittest.main()
