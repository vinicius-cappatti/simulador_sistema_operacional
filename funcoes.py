import csv

def ler_parametros(caminho_csv):
    with open(caminho_csv, mode='r', encoding='utf-8') as arquivo:
        leitor = csv.reader(arquivo, delimiter= ";")
        next(leitor, None)  # Ignora a primeira linha pois ela contem o cabecalho
        parametros = next(leitor, None)  # Le somente a segunda linha que contem os parametros
        return parametros
