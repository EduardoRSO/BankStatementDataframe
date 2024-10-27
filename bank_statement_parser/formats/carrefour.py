import pandas as pd
import re
from datetime import datetime
from bank_statement_parser.formats.parser import Parser

class CarrefourParser(Parser):
    PATTERN = r'^\d{2}/\d{2} .*?\d+$'
    MESES = {
        "jan": "01",
        "fev": "02",
        "mar": "03",
        "abr": "04",
        "mai": "05",
        "jun": "06",
        "jul": "07",
        "ago": "08",
        "set": "09",
        "out": "10",
        "nov": "11",
        "dez": "12"
    }

    def __init__(self, file_path, password_list=None):
        super().__init__(file_path, password_list)
        self.load_category_definitions('Carrefour')
        if self.text != "":
            self.extract_data()
            if self.data != []:
                self.transform_to_dataframe('Carrefour')
                if not self.transformed_data.empty:
                    self.save_transformed_dataframe(self.transformed_data)

    def extract_data(self):
        extracted_lines = re.findall(self.PATTERN, self.text, re.MULTILINE)
        self.data = []
        for line in extracted_lines:
            split_line = line.split(" ")
            dia = split_line[0][0:2]
            mes = self.MESES[self.file_path[-9:-6]]
            ano = self.file_path[-6:-4]
            extracted_date = datetime.strptime(f'{dia}/{mes}/{ano}','%d/%m/%y').strftime('%d/%m/%Y')
            extracted_value = '-'+split_line[-1]
            extracted_description = ' '.join(split_line[1:-1])
            tmp = {
                'data_transacao': extracted_date,
                'valor_transacao': extracted_value,
                'descricao_transacao': extracted_description
            }
            self.data.append(tmp)