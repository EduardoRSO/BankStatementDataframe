import pandas as pd
import re
from bank_statement_parser.formats.parser import Parser

class CarrefourParser(Parser):
    PATTERN = r'^\d{2}/\d{2} .*?\d+$'
    RECEITAS_CATEGORIAS = [
        'Salários e Rendimentos', 'Investimentos', 'Freelances e Serviços', 
        'Aluguéis Recebidos', 'Reembolsos e Reversões', 'Prêmios e Concursos', 'Outros Créditos'
    ]
    SALARIOS_RENDIMENTOS = ['salário', 'rendimentos', 'benefício', 'bonus', 'salario']
    INVESTIMENTOS = ['investimento', 'juros', 'dividendo', 'ações', 'ganho capital']
    FREELANCES_SERVICOS = ['freelance', 'serviço', 'consultoria']
    ALUGUEIS_RECEBIDOS = ['aluguel', 'renda locação']
    REEMBOLSOS_REVERSOES = ['reembolso', 'estorno', 'devolução']
    PREMIOS_CONCURSOS = ['prêmio', 'concurso', 'sorteio']
    OUTROS_CREDITOS = ['doação', 'presente', 'outros créditos']
    
    MORADIA = ['aluguel', 'hipoteca', 'luz', 'água', 'energia', 'condomínio', 'serviços domésticos', 'crf', 'p&f mat. construcao']
    TRANSPORTE = ['combustível', 'transporte público', 'manutenção veículo', 'uber', 'táxi', 'mercadocar']
    ALIMENTACAO = ['supermercado', 'restaurante', 'lanche', 'alimentação', 'comida','atacadista', 'carnes', 'comercio','planta e saude']
    EDUCACAO = ['escola', 'curso', 'material escolar', 'universidade']
    SAUDE_BEM_ESTAR = ['saúde', 'medicamento', 'academia', 'médico', 'consulta','garra','otica' ,'oculos', 'megafarma']
    LAZER_ENTRETENIMENTO = ['cinema', 'viagem', 'evento', 'show', 'lazer', 'hobbies']
    VESTUARIO_COMPRAS_PESSOAIS = ['roupa', 'acessório', 'calçado', 'vestuário', 'sapataria']
    IMPOSTOS_TAXAS = ['imposto', 'multa', 'taxa bancária', 'encargos']
    SERVICOS_ASSINATURAS = ['internet', 'assinatura', 'plano', 'tv a cabo', 'celular', 'anuidade']
    OUTROS_DEBITOS = ['outros débitos', 'despesa extra','advocacia']

    def __init__(self, file_path, password_list=None):
        super().__init__(file_path, password_list)
        self.extract_data()
        self.transform_to_dataframe()

    def extract_data(self):
        extracted_lines = re.findall(self.PATTERN, self.text, re.MULTILINE)
        self.data = []
        for line in extracted_lines:
            split_line = line.split(" ")
            tmp = {
                'data_transacao': split_line[0],
                'valor_transacao': split_line[-1],
                'descricao_transacao': ' '.join(split_line[1:-1])
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
        df['categoria_transacao'] = df['descricao_transacao'].apply(self.classificar_categoria)
        df['tipo_hierarquia'] = df['categoria_transacao'].apply(lambda x: 'Receitas' if x in self.RECEITAS_CATEGORIAS else 'Custos')
        df['entrada'] = df.apply(lambda row: abs(row['valor_transacao']) if row['tipo_hierarquia'] == 'Receitas' else 0, axis=1)
        df['saida'] = df.apply(lambda row: abs(row['valor_transacao']) if row['tipo_hierarquia'] == 'Custos' else 0, axis=1)
        df['net'] = df['entrada'] - df['saida']
        df['origem'] = 'Carrefour'
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
