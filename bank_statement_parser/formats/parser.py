import os
import logging
import regex as re
from abc import ABC, abstractmethod
from formats.itau import ItauParser
from formats.caixa import CaixaParser
from formats.bradesco import BradescoParser
from formats.carrefour import CarrefourParser
from bank_statement_parser.utils.pdf_extractor import PDFExtractor

class Parser(ABC):
    """
    Classe abstrata base para os parsers de extratos bancários.
    Define a interface comum para os métodos de extração de dados.
    """

    def __init__(self, file_path):
        self.file_path = file_path

        # Configuração do logger
        self.logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
        # Instância do PDFExtractor
        self.pdf_extractor = PDFExtractor(file_path)
        
        # Extrai o texto do PDF
        self.text = self.pdf_extractor.extract_text()
        
        # Define o caminho do arquivo de saída na pasta 'resultados'
        output_dir = "resultados"
        os.makedirs(output_dir, exist_ok=True)  # Cria a pasta se não existir
        output_path = os.path.join(output_dir, os.path.basename(file_path).replace(".pdf", "_texto_extraido.txt"))

        # Salva o texto extraído em um arquivo na pasta 'resultados'
        self.pdf_extractor.save_text_to_file(output_path)

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
