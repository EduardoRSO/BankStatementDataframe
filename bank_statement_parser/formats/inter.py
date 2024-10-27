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
    SALARIOS_RENDIMENTOS = ['pix recebido']
    INVESTIMENTOS = ['credito evento b3:', 'aplicacao:', 'aplicacao em fundos:', 'cashback fundos:', 'recebimento de juros:', 'credito b3:', 'credito resgate fundo:', 'cashback:','credito tesouro direto:', 'pagamento / rec. juros:', 'cashback cartao de credito', 'vencimento renda fixa:', 'aplicacao transacao sem descricao', 'cred pontos meu porquinho:','aplicacao poupanca transacao sem descricao', 'dep conta intl loop:','cred pontos conta global:', 'deposito:','credito conta global de inv:']
    FREELANCES_SERVICOS = []
    ALUGUEIS_RECEBIDOS = []
    REEMBOLSOS_REVERSOES = ['estorno:']
    PREMIOS_CONCURSOS = []
    OUTROS_CREDITOS = ['antecipacao de recebiveis - bovespa: "de banco inter s/a" r$ 266,51', 'antecipacao de recebiveis - bovespa: "de banco inter s/a" r$ 296,03', 'antecipacao de recebiveis - bovespa: "de banco inter s/a" r$ 3.972,93', 'antecipacao de recebiveis - bovespa: "de banco inter s/a" r$ 640,92,94']
    
    MORADIA = ['pagamento -r$', 'pagamento efetuado', 'compra no debito:', 'boleto recebido:']
    TRANSPORTE = ['shell box - abastecimento:']
    ALIMENTACAO = []
    EDUCACAO = []
    SAUDE_BEM_ESTAR = []
    LAZER_ENTRETENIMENTO = []
    VESTUARIO_COMPRAS_PESSOAIS = ['compra:', 'venda:', 'cred digital boleto:']
    IMPOSTOS_TAXAS = ['imposto:', 'debito iof conta global de inv:', 'iof op conta intl loop:', 'iof:']
    SERVICOS_ASSINATURAS = ['tim s a', 'recarga: "recarga tim"']
    OUTROS_DEBITOS = ['resgate:', 'resgate de fundo:', 'saque:','pix enviado:','debito b3:','debito tesouro direto:','debito fundo:', 'credito liberado: "pix no credito"', 'resgate poupanca transacao sem descricao', 'debito oferta publica:', 'debito conta global de inv:', 'antecipacao de recebiveis - bovespa: "de banco inter s/a" r$ 850,94']

    def __init__(self, file_path, password_list=None):
        super().__init__(file_path, password_list)
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
