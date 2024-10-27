import pandas as pd
import re
from bank_statement_parser.formats.parser import Parser

class CaixaParser(Parser):
    PATTERN = r'^\d{2}/\d{2}/\d{4} .*?,\d{2} [A-Z] .*?,\d{2} [A-Z]'
    RECEITAS_CATEGORIAS = [
        'Salários e Rendimentos', 'Investimentos', 'Freelances e Serviços', 
        'Aluguéis Recebidos', 'Reembolsos e Reversões', 'Prêmios e Concursos', 'Outros Créditos'
    ]
    SALARIOS_RENDIMENTOS = ['cred inss']
    INVESTIMENTOS = []
    FREELANCES_SERVICOS = []
    ALUGUEIS_RECEBIDOS = []
    REEMBOLSOS_REVERSOES = []
    PREMIOS_CONCURSOS = []
    OUTROS_CREDITOS = ['saldo dia', 'cred', 'dp din lot', 'dep din ag', 'dep', 'dp']
    
    MORADIA = ['compra', 'db cx cap', 'luz', 'gas', 'pag boleto', 'cp elo']
    TRANSPORTE = []
    ALIMENTACAO = []
    EDUCACAO = []
    SAUDE_BEM_ESTAR = []
    LAZER_ENTRETENIMENTO = ['ap loteria', 'saque lot']
    VESTUARIO_COMPRAS_PESSOAIS = []
    IMPOSTOS_TAXAS = ['deb iof', 'deb juros']
    SERVICOS_ASSINATURAS = ['db t cesta', 'fone']
    OUTROS_DEBITOS = ['envio pix']

    def __init__(self, file_path, password_list=None):
        super().__init__(file_path, password_list)
        if self.text != "":
            self.extract_data()
            if self.data != []:
                self.transform_to_dataframe('Caixa')
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
