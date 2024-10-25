import os
from bank_statement_parser.formats.itau import ItauParser
from bank_statement_parser.formats.caixa import CaixaParser
from bank_statement_parser.formats.bradesco import BradescoParser
from bank_statement_parser.formats.carrefour import CarrefourParser

class ParserFactory:
    """
    Fábrica para selecionar o parser correto com base no nome do arquivo.
    """
    
    @staticmethod
    def get_parser(file_path, password_list=None):
        file_name = os.path.basename(file_path).lower()

        if "caixa" in file_name:
            return CaixaParser(file_path, password_list)
        elif "bradesco" in file_name:
            return BradescoParser(file_path, password_list)
        elif "carrefour" in file_name:
            return CarrefourParser(file_path, password_list)
        elif "itau" in file_name:
            return ItauParser(file_path, password_list)
        else:
            raise ValueError(f"Nenhum parser disponível para o arquivo: {file_name}")
