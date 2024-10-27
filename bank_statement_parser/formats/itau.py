import re
import pandas as pd
from datetime import datetime
from bank_statement_parser.formats.parser import Parser

class ItauParser(Parser):
    PATTERN = r'^\d{2}/\d{2}$'
    RECEITAS_CATEGORIAS = [
        'Salários e Rendimentos', 'Investimentos', 'Freelances e Serviços', 
        'Aluguéis Recebidos', 'Reembolsos e Reversões', 'Prêmios e Concursos', 'Outros Créditos'
    ]
    SALARIOS_RENDIMENTOS = []
    INVESTIMENTOS = []
    FREELANCES_SERVICOS = []
    ALUGUEIS_RECEBIDOS = []
    REEMBOLSOS_REVERSOES = []
    PREMIOS_CONCURSOS = []
    OUTROS_CREDITOS = []
    
    MORADIA = ['casasba*casas bahi', 'pagto ficha compensacao']
    TRANSPORTE = []
    ALIMENTACAO = []
    EDUCACAO = []
    SAUDE_BEM_ESTAR = []
    LAZER_ENTRETENIMENTO = []
    VESTUARIO_COMPRAS_PESSOAIS = []
    IMPOSTOS_TAXAS = []
    SERVICOS_ASSINATURAS = ['amazon kindle unltd', 'anuidade diferenci', 'google duolingo']
    OUTROS_DEBITOS = ['encargos de atraso']

    def __init__(self, file_path, password_list=None):
        super().__init__(file_path, password_list)
        if self.text != "":
            self.extract_data()
            if self.data != []:
                self.transform_to_dataframe('Itau')
                if not self.transformed_data.empty:
                    self.save_transformed_dataframe(self.transformed_data)

    def extract_data(self):
        stop_conditions = ['Compras parceladas - próximas faturas']
        self.data = []
        splitted_lines = self.text.split('\n')
        curr_pos = 0
        curr_date = ''
        while curr_pos < len(splitted_lines):
            curr_line = splitted_lines[curr_pos]
            if any(re.match(cond, splitted_lines[curr_pos]) for cond in stop_conditions):
                break
            date_match = re.match(self.PATTERN, curr_line)
            if date_match:
                curr_date = date_match.group()
                curr_pos +=1
                curr_description = splitted_lines[curr_pos]
                curr_pos +=1
                curr_value = splitted_lines[curr_pos]
                extracted_date = datetime.strptime(curr_date+"/"+self.file_path[-6:-4],'%d/%m/%y').strftime('%d/%m/%Y')
                extracted_value = '-'+curr_value.replace('-', ' ').strip()
                extracted_description = curr_description.strip()
                tmp = {
                    'data_transacao': extracted_date,
                    'valor_transacao': extracted_value,
                    'descricao_transacao': extracted_description
                }
                self.data.append(tmp)
            curr_pos +=1
