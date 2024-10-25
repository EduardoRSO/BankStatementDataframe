import os
from abc import ABC, abstractmethod
from formats.itau import ItauParser
from formats.caixa import CaixaParser
from formats.bradesco import BradescoParser
from formats.carrefour import CarrefourParser

class Parser(ABC):
    """
    Classe abstrata base para os parsers de extratos bancários.
    Define a interface comum para os métodos de extração de dados.
    """

    def __init__(self, file_path):
        self.file_path = file_path

    @abstractmethod
    def extract_data(self):
        """
        Método abstrato para extrair dados do extrato.
        """
        pass

class ParserFactory:
    """
    Fábrica para selecionar o parser correto com base no nome do arquivo.
    """
    
    @staticmethod
    def get_parser(file_path):
        file_name = os.path.basename(file_path).lower()

        if "caixa" in file_name:
            return CaixaParser(file_path)
        elif "bradesco" in file_name:
            return BradescoParser(file_path)
        elif "carrefour" in file_name:
            return CarrefourParser(file_path)
        elif "itau" in file_name:
            return ItauParser(file_path)
        else:
            raise ValueError(f"Nenhum parser disponível para o arquivo: {file_name}")
