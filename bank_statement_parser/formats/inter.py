import re
import locale
import pandas as pd
from datetime import datetime
from bank_statement_parser.formats.parser import Parser

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

class InterParser(Parser):
    PATTERN = r'.*R\$ \d*\.*\d+,\d+.*R\$ \d*\.*\d+,\d+$'
    RECEITAS_CATEGORIAS = [
        'Salários e Rendimentos', 'Investimentos', 'Freelances e Serviços', 
        'Aluguéis Recebidos', 'Reembolsos e Reversões', 'Prêmios e Concursos', 'Outros Créditos'
    ]
    SALARIOS_RENDIMENTOS = ['credito evento b3:', 'resgate:', 'aplicacao:']
    INVESTIMENTOS = []
    FREELANCES_SERVICOS = []
    ALUGUEIS_RECEBIDOS = []
    REEMBOLSOS_REVERSOES = []
    PREMIOS_CONCURSOS = []
    OUTROS_CREDITOS = ['pix recebido']
    
    MORADIA = ['pagamento -r$']
    TRANSPORTE = []
    ALIMENTACAO = []
    EDUCACAO = []
    SAUDE_BEM_ESTAR = []
    LAZER_ENTRETENIMENTO = []
    VESTUARIO_COMPRAS_PESSOAIS = []
    IMPOSTOS_TAXAS = []
    SERVICOS_ASSINATURAS = ['tim s a']
    OUTROS_DEBITOS = []

    def __init__(self, file_path, password_list=None):
        super().__init__(file_path, password_list)
        if self.text != "":
            self.extract_data()
            if self.data != []:
                self.transform_to_dataframe()
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
            date_match = re.search(r'(\d+ de [A-Za-z]+ de \d{4})', curr_line)
            if date_match:
                curr_date = date_match.group()
            transaction_match = re.search(self.PATTERN, curr_line)
            if transaction_match:
                for remove in removes:
                    curr_line = re.sub(remove,'',curr_line)
                curr_line = curr_line.split(' ')
                tmp = {
                    'data_transacao': datetime.strptime(curr_date, '%d de %B de %Y').strftime('%d/%m/%Y'),
                    'valor_transacao': curr_line[-3],
                    'descricao_transacao': ' '.join(curr_line[0:-2])
                }
                self.data.append(tmp)
            curr_pos +=1

    def transform_to_dataframe(self):
        df = pd.DataFrame(self.data)
        df.rename(columns={
            'data_transacao': 'data_transacao',
            'valor_transacao': 'valor_transacao',
            'descricao_transacao': 'descricao_transacao'
        }, inplace=True)
        
        df['valor_transacao'] = pd.to_numeric(df['valor_transacao'].str.replace('.', '').str.replace(',', '.').str.replace('-', '').str.strip())
        df['categoria_transacao'] = df['descricao_transacao'].apply(self.classificar_categoria)
        df['tipo_hierarquia'] = df['categoria_transacao'].apply(lambda x: 'Receitas' if x in self.RECEITAS_CATEGORIAS else 'Custos')
        df['entrada'] = df.apply(lambda row: abs(row['valor_transacao']) if row['tipo_hierarquia'] == 'Receitas' else 0, axis=1)
        df['saida'] = df.apply(lambda row: abs(row['valor_transacao']) if row['tipo_hierarquia'] == 'Custos' else 0, axis=1)
        df['net'] = df['entrada'] - df['saida']
        df['origem'] = 'Inter'
        self.transformed_data = df

    def classificar_categoria(self, descricao):
        descricao = descricao.lower()
        
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
        elif any(word in descricao for word in self.MORADIA):
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
