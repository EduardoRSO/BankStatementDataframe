import pandas as pd
import re
from bank_statement_parser.formats.parser import Parser

class BradescoParser(Parser):
    PATTERN = r"Data Histórico Docto\. Crédito \(R\$\) Débito \(R\$\) Saldo \(R\$\)"

    RECEITAS_CATEGORIAS = [
        'Salários e Rendimentos', 'Investimentos', 'Freelances e Serviços', 
        'Aluguéis Recebidos', 'Reembolsos e Reversões', 'Prêmios e Concursos', 'Outros Créditos'
    ]
    SALARIOS_RENDIMENTOS = ['rendimentos poup facil-depos', 'transf saldo c/sal p/cc', 'credito de salario bco:']
    INVESTIMENTOS = []
    FREELANCES_SERVICOS = []
    ALUGUEIS_RECEBIDOS = []
    REEMBOLSOS_REVERSOES = []
    PREMIOS_CONCURSOS = []
    OUTROS_CREDITOS = ['rem: napoleao ribeiro silv 24/06', 'transferencia pix rem: maria amelia mendes d 24/06']
    
    MORADIA = ['kaue boretti de lana', 'eletron']
    TRANSPORTE = []
    ALIMENTACAO = []
    EDUCACAO = ['caixa de cursos ltda']
    SAUDE_BEM_ESTAR = []
    LAZER_ENTRETENIMENTO = []
    VESTUARIO_COMPRAS_PESSOAIS = []
    IMPOSTOS_TAXAS = ['estorno de rendimentos * poup facil-depos']
    SERVICOS_ASSINATURAS = []
    OUTROS_DEBITOS = ['eduardo ribeiro silva 22/10', 'napoleao ribeiro silv 22/10', 'pix qr code estatico des: napoleao ribeiro silv 13/09']

    def __init__(self, file_path, password_list=None):
        super().__init__(file_path, password_list)
        self.extract_data()
        self.transform_to_dataframe()
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
        df['origem'] = 'Bradesco'
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
