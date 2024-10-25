from bank_statement_parser.formats.parser import Parser

class CarrefourParser(Parser):

    def __init__(self, file_path, password_list=None):
        # Chama o construtor da classe pai (Parser) para inicializar os atributos
        super().__init__(file_path, password_list)

    def extract_data(self):
        # Implementação específica para extrair dados do extrato Carrefour
        print("Extraindo dados do extrato Carrefour")
