import PyPDF2
import logging

class PDFExtractor:
    def __init__(self, pdf_path: str):
        """
        Classe responsável pela extração de texto de arquivos PDF.
        
        Args:
        - pdf_path (str): Caminho do arquivo PDF.
        """
        self.pdf_path = pdf_path
        self.text = ""

        # Configurando o logger para a classe
        self.logger = logging.getLogger("PDFExtractor")
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    def extract_text(self) -> str:
        """
        Extrai o texto de todas as páginas do PDF especificado no pdf_path.

        Returns:
        - str: Texto extraído do PDF.
        """
        try:
            with open(self.pdf_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                num_pages = len(reader.pages)  # Obter o número total de páginas
                self.logger.debug(f"Total de páginas no PDF: {num_pages}")
                
                # Percorre todas as páginas do PDF
                for page_num in range(num_pages):
                    page = reader.pages[page_num]
                    page_text = page.extract_text()  # Extraindo texto da página
                    if page_text:
                        self.text += page_text  # Adiciona o texto da página
                    else:
                        self.logger.warning(f"A página {page_num + 1} não contém texto extraído.")
            
            return self.text
        except Exception as e:
            self.logger.error(f"Erro ao extrair texto do PDF: {e}")
            return ""

    def save_text_to_file(self, output_path: str):
        """
        Salva o texto extraído do PDF em um arquivo de texto.

        Args:
        - output_path (str): Caminho onde o arquivo de texto será salvo.
        """
        if not self.text:
            self.logger.warning("Nenhum texto extraído. Execute 'extract_text()' primeiro.")
            return

        try:
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(self.text)
            self.logger.debug(f"Texto salvo em: {output_path}")
        except Exception as e:
            self.logger.error(f"Erro ao salvar o texto: {e}")
