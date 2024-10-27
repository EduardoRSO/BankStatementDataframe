import pandas as pd
import re
from bank_statement_parser.formats.parser import Parser

class BradescoParser(Parser):
    PATTERN = r"Data Histórico Docto\. Crédito \(R\$\) Débito \(R\$\) Saldo \(R\$\)"

    def __init__(self, file_path, password_list=None):
        super().__init__(file_path, password_list)
        self.load_category_definitions('Bradesco')
        if self.text != "":
            self.extract_data()
            if self.data != []:
                self.transform_to_dataframe('Bradesco')
                if not self.transformed_data.empty:
                    self.save_transformed_dataframe(self.transformed_data)


    def extract_data(self):
        stop_conditions = [r"Data Histórico Docto\. Crédito \(R\$\) Débito \(R\$\) Saldo \(R\$\)", r"Data: ", r"Total \d+,\d+ \d+,\d+$"]
        self.data = []
        splitted_lines = self.text.split('\n')
        curr_pos = 0
        while curr_pos < len(splitted_lines)-1:
            curr_date = ''
            line = splitted_lines[curr_pos]
            if re.match(self.PATTERN,line):
                curr_pos +=1
                while not any(re.match(cond, splitted_lines[curr_pos]) for cond in stop_conditions):
                    curr_line = str(splitted_lines[curr_pos] + splitted_lines[curr_pos+1]).replace('\n',' ')
                    transaction_match = re.search(r'\d+,\d+\s*$', curr_line.strip())
                    if transaction_match:
                        date_match = re.match(r'^\d{2}/\d{2}/\d{4}', curr_line) 
                        if date_match:
                            curr_date = date_match.group()
                            curr_line = curr_line.replace(curr_date, "")
                        curr_line = curr_line.split(" ")
                        tmp = {
                            'data_transacao': curr_date,
                            'valor_transacao': curr_line[-2],
                            'descricao_transacao': ' '.join(curr_line[0:-2])
                        }
                        self.data.append(tmp)
                    curr_pos +=1
            else:
                curr_pos +=1