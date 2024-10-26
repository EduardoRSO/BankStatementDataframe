from setuptools import setup, find_packages

# Function to read dependencies from requirements.txt
def parse_requirements(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().splitlines()

setup(
    name="BankStatementParser",
    version="0.1.0",
    description="Uma ferramenta para extrair dados de extratos bancários em PDF e transformá-los em DataFrame para integração em dashboards.",
    author="EduardoRSO",
    author_email="edusillva784@gmail.com",
    url="https://github.com/EduardoRSO/BankStatementParser",
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),  # Read dependencies from requirements.txt
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12.0',
)
