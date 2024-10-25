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

        # Configuração do logger
        self.logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
        # Instância do PDFExtractor com a lista de senhas
        self.pdf_extractor = PDFExtractor(file_path, self.password_list)
        
        # Extrai o texto do PDF usando as senhas fornecidas
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