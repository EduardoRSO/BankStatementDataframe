import os
import unittest
from bank_statement_parser.formats.parser_factory import ParserFactory, ItauParser, CaixaParser, BradescoParser, CarrefourParser

class TestParserFactory(unittest.TestCase):

    def setUp(self):
        """
        Configura arquivos PDF para cada tipo de parser com senhas específicas.
        """
        self.files = {
            "caixa_extrato.pdf": "senha_caixa",
            "bradesco_extrato.pdf": "senha_bradesco",
            "carrefour_extrato.pdf": "senha_carrefour",
            "itau_extrato.pdf": "senha_itau"
        }

    def test_parser_selection(self):
        """
        Testa se o ParserFactory retorna a instância correta do parser com base no nome do arquivo.
        """
        for file_name, password in self.files.items():
            parser = ParserFactory.get_parser(file_name, password_list=[password])

            expected_parser_class = {
                "caixa_extrato.pdf": CaixaParser,
                "bradesco_extrato.pdf": BradescoParser,
                "carrefour_extrato.pdf": CarrefourParser,
                "itau_extrato.pdf": ItauParser
            }[file_name]

            self.assertIsInstance(parser, expected_parser_class, f"O parser para {file_name} não é da classe esperada.")

if __name__ == "__main__":
    unittest.main()
