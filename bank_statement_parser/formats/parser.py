import os
import logging
import regex as re
from abc import ABC, abstractmethod
from bank_statement_parser.utils.pdf_extractor import PDFExtractor

class Parser(ABC):
    """
    Classe abstrata base para os parsers de extratos bancários.
    Define a interface comum para os métodos de extração de dados.
    """

    def __init__(self, file_path, password_list=None):
        self.file_path = file_path
        self.password_list = password_list if password_list else []  # Lista de senhas
        self.logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.pdf_extractor = PDFExtractor(file_path, self.password_list)
        self.text = self.pdf_extractor.extract_text()
        os.makedirs("resultados", exist_ok=True)
        output_path = os.path.join("resultados", os.path.basename(file_path.lower()).replace(".pdf", "_texto_extraido.txt"))
        self.pdf_extractor.save_text_to_file(output_path)

    @abstractmethod
    def extract_data(self):
        """
        Método abstrato para extrair dados do extrato.
        """
        pass