import pandas as pd
import re
from bank_statement_parser.formats.parser import Parser

class MercadoPagoParser(Parser):
    PATTERN = r'(^\d{2}-\d{2}-\d{4}\s*((.|\n)*?) R\$ .* R\$ \d*\.*\d+,\d{2})'

    def __init__(self, file_path, password_list=None):
        super().__init__(file_path, password_list)
        self.load_category_definitions('MercadoPago')
        if self.text != "":
            self.extract_data()
            if self.data != []:
                self.transform_to_dataframe('MercadoPago')
                if not self.transformed_data.empty:
                    self.save_transformed_dataframe(self.transformed_data)

    def extract_data(self):
        extracted_lines = re.findall(self.PATTERN, self.text, re.MULTILINE)
        self.data = []
        for line in extracted_lines:
            line = line[0]
            line = line.replace('\n','')
            extracted_date = re.match(r'\d{2}-\d{2}-\d{4}',line).group(0)
            line = line.replace(extracted_date,'').strip()
            line = line.split(' ')
            extracted_value = line[-3] 
            extracted_description = ' '.join(line[0:-4])
            tmp = {
                'data_transacao': extracted_date,
                'valor_transacao': extracted_value,
                'descricao_transacao': extracted_description
            }
            self.data.append(tmp)
