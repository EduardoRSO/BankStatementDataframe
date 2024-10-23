from setuptools import setup, find_packages

setup(
    name="BankStatementParser",
    version="0.1.0",
    description="Uma ferramenta para extrair dados de extratos bancários em PDF e transformá-los em DataFrame para integração em dashboards.",
    author="EduardoRSO",
    author_email="edusillva784@gmail.com",
    url="https://github.com/EduardoRSO/BankStatementParser",
    packages=find_packages(),
    install_requires=[
        # Dependências serão preenchidas ao final do projeto
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12.0',
)
