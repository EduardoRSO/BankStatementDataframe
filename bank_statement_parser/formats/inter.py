import re
import locale
import pandas as pd
from datetime import datetime
from bank_statement_parser.formats.parser import Parser

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

class InterParser(Parser):
    PATTERN = r'.*R\$ \d*\.*\d+,\d+.*R\$ \d*\.*\d+,\d+$'

    def __init__(self, file_path, password_list=None):
        super().__init__(file_path, password_list)
        self.load_category_definitions('Inter')
        if self.text != "":
            self.extract_data()
            if self.data != []:
                self.transform_to_dataframe('Inter')
                if not self.transformed_data.empty:
                    self.save_transformed_dataframe(self.transformed_data)

    def extract_data(self):
        removes = [r'SAC: .*: \d{4} \d{3} \d{4}']
        self.data = []
        splitted_lines = self.text.split('\n')
        curr_pos = 0
        curr_date = ''
        while curr_pos < len(splitted_lines):
            curr_line = splitted_lines[curr_pos]
            for remove in removes:
                curr_line = re.sub(remove,'',curr_line)
            date_match = re.search(r'(\d|\d{2}) de [A-Za-z]+ de \d{4}', curr_line)
            if date_match:
                curr_date = date_match.group()
            transaction_match = re.search(self.PATTERN, curr_line)
            if transaction_match:
                curr_line = curr_line.split(' ')
                extracted_date = datetime.strptime(curr_date, '%d de %B de %Y').strftime('%d/%m/%Y')
                extracted_value = ''.join(curr_line[-4:-2]).lower().replace('r$','')
                extracted_description = ' '.join(curr_line[0:-4])
                tmp = {
                    'data_transacao': extracted_date,
                    'valor_transacao': extracted_value,
                    'descricao_transacao': extracted_description
                }
                self.data.append(tmp)
            curr_pos +=1
