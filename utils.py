import csv

def ler_config(caminho_csv: str):
    """
    Lê os parâmetros do sistema de um arquivo CSV.
    """
    config = {}
    with open(caminho_csv, 'r') as f:
        leitor_csv = csv.reader(f, delimiter=';')
        try:
            next(leitor_csv)  # Pula o cabeçalho
        except StopIteration:
            return config  # Retorna config vazio se o arquivo estiver vazio
        for linha in leitor_csv:
            if len(linha) >= 2:
                config[linha[0]] = linha[1]
            else:
                print(f"Aviso: Linha ignorada por ter menos de duas colunas: {linha}")
    return config