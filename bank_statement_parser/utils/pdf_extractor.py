import PyPDF2
import logging
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

class PDFExtractor:
    USER_PASSWORD = 1
    OWNER_PASSWORD = 2

    def __init__(self, pdf_path: str, password_list=None):
        """
        Classe responsável pela extração de texto de arquivos PDF.

        Args:
        - pdf_path (str): Caminho do arquivo PDF.
        - password_list (list): Lista de senhas para tentar desbloquear o PDF.
        """
        self.pdf_path = pdf_path
        self.text = ""
        self.password_list = password_list if password_list else []

        # Configurando o logger para a classe
        self.logger = logging.getLogger("PDFExtractor")
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # Desabilitar logs de debug de bibliotecas externas
        logging.getLogger("PyPDF2").setLevel(logging.WARNING)

        # Remover a senha se o PDF estiver protegido
        self.remove_pdf_password()

    def remove_pdf_password(self):
        """
        Remove a senha do PDF, caso esteja protegido, e salva o arquivo sem senha no mesmo caminho.
        """
        try:
            with open(self.pdf_path, "rb") as input_file:
                reader = PyPDF2.PdfReader(input_file)

                # Verifica se o PDF está criptografado
                if reader.is_encrypted:
                    self.logger.info(f"O PDF está protegido por senha. Tentando desbloquear: {self.pdf_path}")

                    # Tentar todas as senhas fornecidas
                    for password in self.password_list:
                        result = reader.decrypt(password)
                        if result == self.USER_PASSWORD or result == self.OWNER_PASSWORD:
                            self.logger.info(f"Senha correta encontrada: {password}")
                            break
                    else:
                        raise ValueError("Nenhuma senha fornecida é válida para este PDF.")

                    # Extrair todo o texto do PDF
                    extracted_text = ""
                    for page_num in range(len(reader.pages)):
                        page = reader.pages[page_num]
                        page_text = page.extract_text()
                        if page_text:
                            extracted_text += page_text.strip() + "\n"

                    # Salvar o arquivo descriptografado com o sufixo _descriptografado.pdf
                    new_pdf_path = self.pdf_path.replace(".PDF", "_descriptografado.pdf").replace(".pdf", "_descriptografado.pdf")

                    packet = io.BytesIO()
                    can = canvas.Canvas(packet, pagesize=letter)

                    # Adicionar o texto completo ao PDF
                    can.drawString(10, 750, extracted_text)
                    can.save()

                    # Salvar o PDF no arquivo
                    with open(new_pdf_path, "wb") as output_file:
                        output_file.write(packet.getvalue())

                    self.logger.info(f"PDF salvo sem senha com o texto completo: {new_pdf_path}")

                else:
                    self.logger.info(f"O PDF já está sem senha: {self.pdf_path}")

        except Exception as e:
            self.logger.error(f"Erro ao remover a senha do PDF: {e}")

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
                self.logger.info(f"Total de páginas no PDF: {num_pages}")
                
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
            self.logger.info(f"Texto salvo em: {output_path}")
        except Exception as e:
            self.logger.error(f"Erro ao salvar o texto: {e}")
