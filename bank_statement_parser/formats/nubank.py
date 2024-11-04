import pandas as pd
import re
from bank_statement_parser.formats.parser import Parser

class NubankParser(Parser):
    PATTERN = r'^\d{2}/\d{2}/\d{4} .*?,\d{2} [A-Z] .*?,\d{2} [A-Z]'

    def __init__(self, file_path, password_list=None):
        super().__init__(file_path, password_list)
        self.load_category_definitions('Nubank')
        if self.text != "":
            self.extract_data()
            if self.data != []:
                self.transform_to_dataframe('Nubank')
                if not self.transformed_data.empty:
                    self.save_transformed_dataframe(self.transformed_data)

    def extract_data(self):
        extracted_lines = re.findall(self.PATTERN, self.text, re.MULTILINE)
        self.data = []
        for line in extracted_lines:
            split_line = line.split(" ")
            extracted_date = split_line[0]
            extracted_value = split_line[-4] if split_line[-3] == 'C' else '-'+split_line[-4] 
            extracted_description = ' '.join(split_line[2:-4])
            tmp = {
                'data_transacao': extracted_date,
                'valor_transacao': extracted_value,
                'descricao_transacao': extracted_description
            }
            self.data.append(tmp)
