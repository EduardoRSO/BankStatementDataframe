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
    
    MORADIA = ['crf 3 spp pinheiros -', 'assai atacadista,sao paulo-', 'crf 48 spg giovanni gronc', 'shekinah comercio de m, sao paulo', 'maravilha carnes parqu, sao paulo', 'p&f mat. construcao, sao paulo', 'duda gas, sao paulo', 'akki atacadista, sao paulo', 'assai atacadista, sao paulo']
    TRANSPORTE = []
    ALIMENTACAO = []
    EDUCACAO = ['htm*cursoclpeihm,coronel fabr-']
    SAUDE_BEM_ESTAR = ['academia sempre viva i,sao paulo-', 'pg *ton garra de agu,sao paulo-', 'planta e saude, sao paulo', 'megafarma, sao paulo']
    LAZER_ENTRETENIMENTO = []
    VESTUARIO_COMPRAS_PESSOAIS = ['otica bom preco,sao paulo-', 'agpsapataria, sao paulo', 'fabrica de oculos,sao paulo-']
    IMPOSTOS_TAXAS = []
    SERVICOS_ASSINATURAS = ['anuidade diferenciada -']
    OUTROS_DEBITOS = ['advocacia dgl,maringa-', 'mercadocar, sao paulo']

    def __init__(self, file_path, password_list=None):
        super().__init__(file_path, password_list)
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