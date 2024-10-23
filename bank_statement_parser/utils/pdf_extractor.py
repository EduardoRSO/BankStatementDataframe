import PyPDF2

class PDFExtractor:
    def __init__(self, pdf_path: str):
        """
        Classe responsável pela extração de texto de arquivos PDF.
        
        Args:
        - pdf_path (str): Caminho do arquivo PDF.
        """
        self.pdf_path = pdf_path
        self.text = ""

    def extract_text(self) -> str:
        """
        Extrai o texto do PDF especificado no pdf_path.

        Returns:
        - str: Texto extraído do PDF.
        """
        try:
            with open(self.pdf_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page_num in range(len(reader.pages)):
                    self.text += reader.pages[page_num].extract_text()
            return self.text
        except Exception as e:
            print(f"Erro ao extrair texto do PDF: {e}")
            return ""

    def save_text_to_file(self, output_path: str):
        """
        Salva o texto extraído do PDF em um arquivo de texto.

        Args:
        - output_path (str): Caminho onde o arquivo de texto será salvo.
        """
        if not self.text:
            print("Nenhum texto extraído. Execute 'extract_text()' primeiro.")
            return

        try:
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(self.text)
            print(f"Texto salvo em: {output_path}")
        except Exception as e:
            print(f"Erro ao salvar o texto: {e}")
