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
                self.transform_to_dataframe()
                if not self.transformed_data.empty:
                    self.save_transformed_dataframe(self.transformed_data)


    def extract_data(self):
        stop_conditions = [r"Data Histórico Docto\. Crédito \(R\$\) Débito \(R\$\) Saldo \(R\$\)", r"Data: ", r"Total \d*\.*\d+,\d+ \d*\.*\d+,\d+"]
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
                    if any(re.search(cond,curr_line) for cond in stop_conditions):
                        break
                    transaction_match = re.search(r'\d+,\d+\s*$', curr_line.strip())
                    if transaction_match:
                        date_match = re.match(r'^\d{2}/\d{2}/\d{4}', curr_line) 
                        if date_match:
                            curr_date = date_match.group()
                            curr_line = curr_line.replace(curr_date, "")
                        splitted_line = curr_line.split(" ")
                        extracted_date = curr_date
                        extracted_value = splitted_line[-2]
                        extracted_description = ' '.join(splitted_line[0:-2])
                        tmp = {
                            'data_transacao': extracted_date,
                            'valor_transacao': extracted_value,
                            'descricao_transacao': extracted_description
                        }
                        self.data.append(tmp)
                    curr_pos +=1
            else:
                curr_pos +=1

    def transform_to_dataframe(self):
        df = pd.DataFrame(self.data)
        df.rename(columns={
            'data_transacao': 'data_transacao',
            'valor_transacao': 'valor_transacao',
            'descricao_transacao': 'descricao_transacao'
        }, inplace=True)  
        df['valor_transacao'] = pd.to_numeric(df['valor_transacao'].str.replace('.', '').str.replace(',', '.').str.strip())
        df['categoria_transacao'] = df.apply(self.classificar_categoria, axis=1)
        df['tipo_hierarquia'] = df['categoria_transacao'].apply(lambda x: 'Receitas' if x in self.receitas_definitions.keys() else 'Custos')
        df['entrada'] = df.apply(lambda x: abs(x['valor_transacao']) if x['tipo_hierarquia'] == 'Receitas' else 0, axis=1)
        df['saida'] = df.apply(lambda x: abs(x['valor_transacao']) if x['tipo_hierarquia'] != 'Receitas' else 0, axis=1)
        df['net'] = df['entrada'] - df['saida']
        df['origem'] = 'Bradesco'
        self.transformed_data = df

    def classificar_categoria(self, row: pd.DataFrame):
        descricao = row['descricao_transacao'].lower()
        definitions = self.receitas_definitions 
        for category, keywords in definitions.items():
            if any(word in descricao for word in keywords):
                return category
        definitions = self.custos_definitions 
        for category, keywords in definitions.items():
            if any(word in descricao for word in keywords):
                return category
        return 'Outros'