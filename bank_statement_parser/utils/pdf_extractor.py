import PyPDF2
import logging
import pdfplumber
import os

class PDFExtractor:
    USER_PASSWORD = 1
    OWNER_PASSWORD = 2

    def __init__(self, pdf_path: str, password_list=None):
        self.pdf_path = pdf_path
        self.text = ""
        self.password_list = password_list if password_list else []
        self.decrypted_file_created = False  # Booleano para indicar se um arquivo descriptografado foi criado

        # Configuração do logger
        self.logger = logging.getLogger("PDFExtractor")
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.getLogger("PyPDF2").setLevel(logging.WARNING)

        # Remover a senha se o PDF estiver protegido
        self.remove_pdf_password()

    def remove_pdf_password(self):
        try:
            with open(self.pdf_path, "rb") as input_file:
                reader = PyPDF2.PdfReader(input_file)
                if reader.is_encrypted:
                    self.logger.info(f"O PDF está protegido por senha. Tentando desbloquear: {self.pdf_path}")
                    for password in self.password_list:
                        result = reader.decrypt(password)
                        if result == self.USER_PASSWORD or result == self.OWNER_PASSWORD:
                            self.logger.info(f"Senha correta encontrada: {password}")
                            break
                    else:
                        raise ValueError("Nenhuma senha fornecida é válida para este PDF.")
                    
                    # Salva o PDF sem senha com o sufixo "_descriptografado.pdf"
                    new_pdf_path = self.pdf_path.replace(".PDF", "_descriptografado.pdf")
                    writer = PyPDF2.PdfWriter()
                    for page in reader.pages:
                        writer.add_page(page)
                    with open(new_pdf_path, "wb") as output_file:
                        writer.write(output_file)

                    self.logger.info(f"PDF salvo sem senha: {new_pdf_path}")
                    self.pdf_path = new_pdf_path
                    self.decrypted_file_created = True  # Indica que o arquivo descriptografado foi criado
                else:
                    self.logger.info(f"O PDF já está sem senha: {self.pdf_path}")
        except Exception as e:
            self.logger.error(f"Erro ao remover a senha do PDF: {e}")

    def extract_text(self) -> str:
        """
        Extrai o texto de todas as páginas do PDF, usando pdfplumber caso PyPDF2 falhe.

        Returns:
        - str: Texto extraído do PDF.
        """
        try:
            with open(self.pdf_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                num_pages = len(reader.pages)
                self.logger.info(f"Total de páginas no PDF: {num_pages}")
                
                for page_num, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        self.text += page_text
                    else:
                        self.logger.warning(f"A página {page_num + 1} não contém texto extraído.")
            
            return self.text
        except Exception as e:
            self.logger.error(f"Erro ao extrair texto com PyPDF2: {e}")
            self.logger.info("Tentando extrair o texto com pdfplumber...")

            # Tentativa com pdfplumber
            try:
                with pdfplumber.open(self.pdf_path) as pdf:
                    for page in pdf.pages:
                        self.text += page.extract_text() or ""
                self.logger.info("Texto extraído com sucesso usando pdfplumber.")
                return self.text
            except Exception as e:
                self.logger.error(f"Erro ao extrair texto com pdfplumber: {e}")
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
        finally:
            # Chama o método para remover o arquivo descriptografado, se necessário
            self.remove_decrypted_file()

    def remove_decrypted_file(self):
        """
        Remove o arquivo descriptografado, se ele foi criado.
        """
        if self.decrypted_file_created and os.path.exists(self.pdf_path):
            try:
                os.remove(self.pdf_path)
                self.logger.info(f"Arquivo descriptografado removido: {self.pdf_path}")
            except Exception as e:
                self.logger.error(f"Erro ao remover o arquivo descriptografado: {e}")
