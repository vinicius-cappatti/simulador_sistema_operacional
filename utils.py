import csv
from typing import List

def ler_parametros(caminho_csv: str) -> List[str]:
    """
    Lê os parâmetros do sistema de um arquivo CSV.
    """
    with open(caminho_csv, mode='r', encoding='utf-8') as arquivo:
        leitor = csv.reader(arquivo, delimiter=";")
        next(leitor, None)  # Ignora a primeira linha (cabeçalho)
        return next(leitor, None)  # Lê a segunda linha (parâmetros)