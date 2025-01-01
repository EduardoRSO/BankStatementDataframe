import os
import logging
import regex as re
import pandas as pd
from abc import ABC, abstractmethod
from bank_statement_parser.utils.pdf_extractor import PDFExtractor
from bank_statement_parser.utils.exception_handler import exception_handler_decorator

class Parser(ABC):
    """
    Classe abstrata base para os parsers de extratos bancários.
    Define a interface comum para os métodos de extração de dados.
    """

    @classmethod
    def exception_handler(cls, func):
        return exception_handler_decorator(func)

    def __init__(self, file_path, password_list=None):
        self.file_path = file_path
        self.base_directory = os.path.dirname(file_path)  # Base directory from file path
        self.password_list = password_list if password_list else []
        self.logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
        # PDF Extraction
        self.pdf_extractor = PDFExtractor(file_path, self.password_list)
        self.text = self.pdf_extractor.extract_text()
        
        # Define 'resultados' path within base directory
        resultados_path = os.path.join(self.base_directory, "resultados")
        os.makedirs(resultados_path, exist_ok=True)
        
        # Save extracted text to 'resultados' folder
        output_path = os.path.join(resultados_path, os.path.basename(file_path.lower()).replace(".pdf", "_texto_extraido.txt"))
        self.pdf_extractor.save_text_to_file(output_path)
        
        self.receitas_definitions = {}
        self.custos_definitions = {}

    @abstractmethod
    def extract_data(self):
        """
        Método abstrato para extrair dados do extrato.
        """
        pass

    def load_category_definitions(self, bank_name):
        """
        Loads category definitions from an Excel file located in the base directory into separate dictionaries 
        for "receitas" and "custos".

        Args:
        - bank_name (str): Name of the bank (e.g., 'Inter', 'Itau', etc.)
        """
        category_file_path = os.path.join(self.base_directory, "categorias_definicoes.xlsx")
        try:
            receitas_sheet = f"{bank_name}_receitas"
            custos_sheet = f"{bank_name}_custos"
            receitas_df = pd.read_excel(category_file_path, sheet_name=receitas_sheet)
            custos_df = pd.read_excel(category_file_path, sheet_name=custos_sheet)
            for category in receitas_df.columns:
                self.receitas_definitions[category] = receitas_df[category].dropna().tolist()
            for category in custos_df.columns:
                self.custos_definitions[category] = custos_df[category].dropna().tolist()
            self.logger.info(f"Category definitions loaded for '{bank_name}' from sheets '{receitas_sheet}' and '{custos_sheet}'")
        
        except Exception as e:
            self.logger.error(f"Error loading category definitions for '{bank_name}': {e}")

    def merge_future_transactions(self, dataframe: pd.DataFrame):
        try:
            # Define o caminho do arquivo Excel
            file_path = os.path.join(self.base_directory, "categorias_definicoes.xlsx")

            # Lê as abas 'Entradas_futuras' e 'Saidas_futuras'
            entradas_futuras_df = pd.read_excel(file_path, sheet_name='Entradas_futuras', dtype=str)
            saidas_futuras_df = pd.read_excel(file_path, sheet_name='Saidas_futuras', dtype=str)
            entradas_futuras_df['data_transacao'] = pd.to_datetime(entradas_futuras_df['data_transacao'], errors='coerce').dt.strftime('%d/%m/%Y')
            saidas_futuras_df['data_transacao'] = pd.to_datetime(saidas_futuras_df['data_transacao'], errors='coerce').dt.strftime('%d/%m/%Y')

            # Combina as transações futuras com o DataFrame atual
            combined_df = pd.concat([dataframe, entradas_futuras_df, saidas_futuras_df]).reset_index(drop=True)
            self.logger.info("Transações futuras combinadas com sucesso.")

            return combined_df
        except Exception as e:
            self.logger.error(f"Erro ao combinar transações futuras: {e}")
            return dataframe

    def save_transformed_dataframe(self, dataframe: pd.DataFrame):
        directory = os.path.join(self.base_directory, "transformed_dataframe")
        file_path = os.path.join(directory, "transformed_dataframe.csv")
        
        os.makedirs(directory, exist_ok=True)
        
        if os.path.exists(file_path):
            existing_df = pd.read_csv(file_path)
            combined_df = pd.concat([existing_df, dataframe]).drop_duplicates().reset_index(drop=True)
        else:
            combined_df = dataframe.drop_duplicates().reset_index(drop=True)

        # Chama a função para combinar com transações futuras
        combined_df = self.merge_future_transactions(combined_df)

        combined_df['descricao_transacao'] = combined_df['descricao_transacao'].str.lower()
        combined_df.to_csv(file_path, index=False)
        self.logger.info(f"Dataframe saved to {file_path}, with duplicates removed.")

    def classificar_categoria(self, row: pd.DataFrame):
        descricao = row['descricao_transacao'].lower()
        definitions = self.receitas_definitions if row['tipo_hierarquia'] == 'Receitas' else self.custos_definitions
        for category, keywords in definitions.items():
            if any(word in descricao for word in keywords):
                return category
        return 'Outros'
    
    def transform_to_dataframe(self, origem: str):
        df = pd.DataFrame(self.data)
        df.rename(columns={
            'data_transacao': 'data_transacao',
            'valor_transacao': 'valor_transacao',
            'descricao_transacao': 'descricao_transacao'
        }, inplace=True)  
        df['valor_transacao'] = pd.to_numeric(df['valor_transacao'].str.replace('.', '').str.replace(',', '.').str.strip())
        df['tipo_hierarquia'] = df['valor_transacao'].apply(lambda x: 'Receitas' if x >= 0 else 'Custos')
        df['categoria_transacao'] = df.apply(self.classificar_categoria, axis=1)
        df['entrada'] = df['valor_transacao'].apply(lambda x: abs(x) if x >= 0 else 0)
        df['saida'] = df['valor_transacao'].apply(lambda x: abs(x) if x < 0 else 0)
        df['net'] = df['entrada'] - df['saida']
        df['origem'] = origem
        self.transformed_data = df
