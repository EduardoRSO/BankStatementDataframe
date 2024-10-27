import os
import logging
import regex as re
import pandas as pd
from abc import ABC, abstractmethod
from bank_statement_parser.utils.pdf_extractor import PDFExtractor

class Parser(ABC):
    """
    Classe abstrata base para os parsers de extratos bancários.
    Define a interface comum para os métodos de extração de dados.
    """

    def __init__(self, file_path, password_list=None):
        self.file_path = file_path
        self.password_list = password_list if password_list else [] 
        self.logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.pdf_extractor = PDFExtractor(file_path, self.password_list)
        self.text = self.pdf_extractor.extract_text()
        os.makedirs("resultados", exist_ok=True)
        output_path = os.path.join("resultados", os.path.basename(file_path.lower()).replace(".pdf", "_texto_extraido.txt"))
        self.pdf_extractor.save_text_to_file(output_path)

    @abstractmethod
    def extract_data(self):
        """
        Método abstrato para extrair dados do extrato.
        """
        pass

    def save_transformed_dataframe(self, dataframe: pd.DataFrame):
        directory = "transformed_dataframe"
        file_path = os.path.join(directory, "transformed_dataframe.csv")

        os.makedirs(directory, exist_ok=True)
        
        if os.path.exists(file_path):
            existing_df = pd.read_csv(file_path)
            combined_df = pd.concat([existing_df, dataframe]).drop_duplicates().reset_index(drop=True)
        else:
            combined_df = dataframe.drop_duplicates().reset_index(drop=True)
        combined_df['descricao_transacao'] = combined_df['descricao_transacao'].str.lower()
        combined_df.to_csv(file_path, index=False)
        self.logger.info(f"Dataframe saved to {file_path}, with duplicates removed.")

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
            
    def transform_to_dataframe(self, origem:str):
        df = pd.DataFrame(self.data)
        df.rename(columns={
            'data_transacao': 'data_transacao',
            'valor_transacao': 'valor_transacao',
            'descricao_transacao': 'descricao_transacao'
        }, inplace=True)
        
        df['valor_transacao'] = pd.to_numeric(df['valor_transacao'].str.replace('.', '').str.replace(',', '.').str.strip())
        df['tipo_hierarquia'] = df['valor_transacao'].apply(lambda x: 'Receitas' if x >= 0 else 'Custos')
        df['categoria_transacao'] = df.apply(self.classificar_categoria,axis=1)
        df['entrada'] = df['valor_transacao'].apply(lambda x: abs(x) if x >= 0 else 0)
        df['saida'] = df['valor_transacao'].apply(lambda x: abs(x) if x < 0 else 0)
        df['net'] = df['entrada'] - df['saida']
        df['origem'] = origem
        self.transformed_data = df