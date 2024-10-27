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
                self.transform_to_dataframe()
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

    def transform_to_dataframe(self):
        df = pd.DataFrame(self.data)
        df.rename(columns={
            'data_transacao': 'data_transacao',
            'valor_transacao': 'valor_transacao',
            'descricao_transacao': 'descricao_transacao'
        }, inplace=True)
        
        df['valor_transacao'] = pd.to_numeric(df['valor_transacao'].str.replace('.', '').str.replace(',', '.').str.replace('-', '').str.strip())
        df['tipo_hierarquia'] = df['valor_transacao'].apply(lambda x: 'Receitas' if x >= 0 else 'Custos')
        df['categoria_transacao'] = df.apply(self.classificar_categoria,axis=1)
        df['entrada'] = df['valor_transacao'].apply(lambda x: abs(x) if x >= 0 else 0)
        df['saida'] = df['valor_transacao'].apply(lambda x: abs(x) if x < 0 else 0)
        df['net'] = df['entrada'] - df['saida']
        df['origem'] = 'Caixa'
        self.transformed_data = df

    def classificar_categoria(self, row:pd.DataFrame):
        descricao = row['descricao_transacao'].lower()
        if row['tipo_hierarquia'] == 'Receitas':
            if any(word in descricao for word in self.SALARIOS_RENDIMENTOS):
                return 'Salários e Rendimentos'
            elif any(word in descricao for word in self.INVESTIMENTOS):
                return 'Investimentos'
            elif any(word in descricao for word in self.FREELANCES_SERVICOS):
                return 'Freelances e Serviços'
            elif any(word in descricao for word in self.ALUGUEIS_RECEBIDOS):
                return 'Aluguéis Recebidos'
            elif any(word in descricao for word in self.REEMBOLSOS_REVERSOES):
                return 'Reembolsos e Reversões'
            elif any(word in descricao for word in self.PREMIOS_CONCURSOS):
                return 'Prêmios e Concursos'
            elif any(word in descricao for word in self.OUTROS_CREDITOS):
                return 'Outros Créditos'
            else:
                return 'Outros'
        if row['tipo_hierarquia'] == 'Custos':
            if any(word in descricao for word in self.MORADIA):
                return 'Moradia'
            elif any(word in descricao for word in self.TRANSPORTE):
                return 'Transporte'
            elif any(word in descricao for word in self.ALIMENTACAO):
                return 'Alimentação'
            elif any(word in descricao for word in self.EDUCACAO):
                return 'Educação'
            elif any(word in descricao for word in self.SAUDE_BEM_ESTAR):
                return 'Saúde e Bem-estar'
            elif any(word in descricao for word in self.LAZER_ENTRETENIMENTO):
                return 'Lazer e Entretenimento'
            elif any(word in descricao for word in self.VESTUARIO_COMPRAS_PESSOAIS):
                return 'Vestuário e Compras Pessoais'
            elif any(word in descricao for word in self.IMPOSTOS_TAXAS):
                return 'Impostos e Taxas'
            elif any(word in descricao for word in self.SERVICOS_ASSINATURAS):
                return 'Serviços e Assinaturas'
            elif any(word in descricao for word in self.OUTROS_DEBITOS):
                return 'Outros Débitos'
            else:
                return 'Outros'
