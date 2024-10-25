import os
import unittest
from PyPDF2 import PdfWriter, PdfReader
from bank_statement_parser.formats.parser_factory import ParserFactory, ItauParser, CaixaParser, BradescoParser, CarrefourParser
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

class TestParserFactory(unittest.TestCase):

    def setUp(self):
        """
        Cria arquivos PDF protegidos por senha para cada tipo de parser.
        """
        self.test_text = "Texto de teste para extração"
        self.files = {
            "caixa_extrato.pdf": "senha_caixa",
            "bradesco_extrato.pdf": "senha_bradesco",
            "carrefour_extrato.pdf": "senha_carrefour",
            "itau_extrato.pdf": "senha_itau"
        }

        # Cria cada arquivo PDF com o texto e a senha de teste
        for file_name, password in self.files.items():
            # Gera o PDF com texto usando reportlab
            c = canvas.Canvas(file_name, pagesize=A4)
            c.drawString(100, 750, self.test_text)
            c.save()

            # Lê o PDF gerado e adiciona ao PdfWriter para criptografar
            writer = PdfWriter()
            with open(file_name, "rb") as f:
                reader = PdfReader(f)
                writer.add_page(reader.pages[0])
                writer.encrypt(password)

            # Salva o PDF criptografado
            with open(file_name, "wb") as f:
                writer.write(f)

    def test_password_protected_pdfs(self):
        """
        Testa se o ParserFactory retorna a instância correta e extrai o texto esperado de cada PDF protegido.
        """
        for file_name, password in self.files.items():
            parser = ParserFactory.get_parser(file_name, password_list=[password])

            expected_parser_class = {
                "caixa_extrato.pdf": CaixaParser,
                "bradesco_extrato.pdf": BradescoParser,
                "carrefour_extrato.pdf": CarrefourParser,
                "itau_extrato.pdf": ItauParser
            }[file_name]
            self.assertIsInstance(parser, expected_parser_class)
            self.assertEqual(parser.text.replace('\n',''), self.test_text, f"Texto extraído do {file_name} não corresponde ao texto esperado.")

    def tearDown(self):
        """
        Remove os arquivos PDF criados para os testes.
        """
        for file_name in self.files:
            if os.path.exists(file_name):
                # os.remove(file_name)
                pass

if __name__ == "__main__":
    unittest.main()
