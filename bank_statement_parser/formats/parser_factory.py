import os
from bank_statement_parser.formats.itau import ItauParser
from bank_statement_parser.formats.inter import InterParser
from bank_statement_parser.formats.caixa import CaixaParser
from bank_statement_parser.formats.nubank import NubankParser
from bank_statement_parser.formats.bradesco import BradescoParser
from bank_statement_parser.formats.carrefour import CarrefourParser
from bank_statement_parser.formats.mercadopago import MercadoPagoParser

class ParserFactory:
    """
    Fábrica para selecionar o parser correto com base no nome do arquivo.
    """
    
    @staticmethod
    def get_parser(file_path, password_list=None):
        if "caixa" in file_path:
            return CaixaParser(file_path, password_list)
        elif "bradesco" in file_path:
            return BradescoParser(file_path, password_list)
        elif "carrefour" in file_path:
            return CarrefourParser(file_path, password_list)
        elif "itau" in file_path:
            return ItauParser(file_path, password_list)
        elif "inter" in file_path:
            return InterParser(file_path, password_list)
        elif "mercadopago" in file_path:
            return MercadoPagoParser(file_path, password_list)
        elif "nubank" in file_path:
            return NubankParser(file_path, password_list)
        else:
            raise ValueError(f"Nenhum parser disponível para o arquivo: {file_path}")
