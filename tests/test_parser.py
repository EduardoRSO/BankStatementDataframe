import os
import unittest
from PyPDF2 import PdfWriter
from bank_statement_parser.formats.parser_factory import ParserFactory, ItauParser, CaixaParser, BradescoParser, CarrefourParser

class TestParserFactory(unittest.TestCase):

    def setUp(self):
        """
        Cria arquivos PDF protegidos por senha para cada tipo de parser.
        """
        self.test_text = "Texto de teste para extração."
        self.files = {
            "caixa_extrato.pdf": "senha_caixa",
            "bradesco_extrato.pdf": "senha_bradesco",
            "carrefour_extrato.pdf": "senha_carrefour",
            "itau_extrato.pdf": "senha_itau"
        }

        # Cria cada arquivo PDF com a senha e o texto de teste
        for file_name, password in self.files.items():
            writer = PdfWriter()
            writer.add_blank_page(width=595.28, height=841.89)
            writer.encrypt(password)
            
            # Adiciona uma página com o texto de teste
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

            # Verifica se o parser correto foi instanciado
            self.assertIsInstance(parser, expected_parser_class)
            # Verifica se o texto extraído é o esperado
            self.assertEqual(parser.text, self.test_text, f"Texto extraído do {file_name} não corresponde ao texto esperado.")

    def tearDown(self):
        """
        Remove os arquivos PDF criados para os testes.
        """
        for file_name in self.files:
            if os.path.exists(file_name):
                os.remove(file_name)

if __name__ == "__main__":
    unittest.main()
