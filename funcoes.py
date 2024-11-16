import csv
from typing import List, Dict

class Frame:
    """
    Representa um frame na memória física.
    """
    def __init__(self, id: int):
        self.id = id                # ID do frame na memória física
        self.ocupado = False        # Indica se o frame está ocupado
        self.id_processo = None     # ID do processo que ocupa o frame (se ocupado)
        self.id_pagina = None       # ID da página que ocupa o frame (se ocupado)
        self.dados = None           # Dados armazenados no frame

    def isOcupado(self):
        """Verifica se o frame está ocupado."""
        return self.ocupado

class PageTable:
    """
    Representa a tabela de páginas de um processo.
    """
    def __init__(self, num_paginas: int, tamanho_pagina: int):
        # Inicializa a tabela com None para cada página
        self.tabela: List[Frame] = [None] * num_paginas
        self.tamanho_pagina = tamanho_pagina

    def traduzir_endereco_virtual(self, end_vir: int) -> tuple:
        """
        Traduz um endereço virtual para um número de página e deslocamento.
        Retorna uma tupla (numero_pagina, deslocamento).
        """
        numero_pagina = end_vir // self.tamanho_pagina
        deslocamento = end_vir % self.tamanho_pagina
        return (numero_pagina, deslocamento)

    def obter_frame(self, numero_pagina: int) -> Frame:
        """
        Retorna o frame associado a uma página específica.
        """
        if 0 <= numero_pagina < len(self.tabela):
            return self.tabela[numero_pagina]
        return None

    def armazena(self, processo: 'Processo', dado: str, end_vir: int):
        """
        Armazena um dado em um endereço virtual específico.
        """
        numero_pagina, deslocamento = self.traduzir_endereco_virtual(end_vir)
        if 0 <= numero_pagina < len(self.tabela):
            frame = self.tabela[numero_pagina]
            if frame:
                frame.ocupado = True
                frame.id_processo = processo.pid
                frame.id_pagina = numero_pagina
                frame.dados = dado
            else:
                raise Exception(f"Não há frame associado à página {numero_pagina}")
        else:
            raise Exception(f"Endereço virtual {end_vir} inválido")

    def existe(self, end_vir: int) -> bool:
        """
        Verifica se existe um mapeamento para o endereço virtual.
        """
        numero_pagina, _ = self.traduzir_endereco_virtual(end_vir)
        return 0 <= numero_pagina < len(self.tabela) and self.tabela[numero_pagina] is not None

class Processo:
    """
    Representa um processo no sistema.
    """
    def __init__(self, pid: int, tamanho: int, tamanho_pagina: int):
        self.pid = pid
        self.tamanho = tamanho
        self.tamanho_pagina = tamanho_pagina
        num_paginas = (tamanho + tamanho_pagina - 1) // tamanho_pagina
        self.tab_pags = PageTable(num_paginas, tamanho_pagina)
        self.memo_virtual = list(range(tamanho))

    def acessar_dados(self, endereco_acessado: int) -> str:
        """
        Acessa os dados em um endereço virtual específico.
        """
        if not self.tab_pags.existe(endereco_acessado):
            raise Exception(f"Página para o endereço {endereco_acessado} não está na memória física")
        
        numero_pagina, deslocamento = self.tab_pags.traduzir_endereco_virtual(endereco_acessado)
        frame = self.tab_pags.obter_frame(numero_pagina)
        if not frame.isOcupado() or frame.id_processo != self.pid:
            raise Exception(f"Acesso inválido ao endereço {endereco_acessado}")
        
        return frame.dados

class MemFis:
    """
    Representa a memória física do sistema.
    """
    def __init__(self, tam_mem_fis: int, id_frm_ini: int, tam_frm: int):
        self.memoria: List[Frame] = [Frame(id_frm_ini + i * tam_frm) for i in range(tam_mem_fis)]
        self.firstIn = 0  # Índice para política de substituição FIFO

    def isFull(self) -> bool:
        """Verifica se a memória física está cheia."""
        return all(frame.isOcupado() for frame in self.memoria)

    def findLivre(self) -> Frame:
        """Encontra o primeiro frame livre na memória física."""
        for frame in self.memoria:
            if not frame.isOcupado():
                return frame
        return None

def ler_parametros(caminho_csv: str) -> List[str]:
    """
    Lê os parâmetros do sistema de um arquivo CSV.
    """
    with open(caminho_csv, mode='r', encoding='utf-8') as arquivo:
        leitor = csv.reader(arquivo, delimiter=";")
        next(leitor, None)  # Ignora a primeira linha (cabeçalho)
        return next(leitor, None)  # Lê a segunda linha (parâmetros)

def print_status(memo_fis: MemFis):
    """
    Imprime o status atual da memória física.
    """
    for frame in memo_fis.memoria:
        if frame.isOcupado():
            print(f"Frame {frame.id}: Processo {frame.id_processo}, Página {frame.id_pagina}")
        else:
            print(f"Frame {frame.id}: Livre")

def carregarPag(memo_fis: MemFis, proc: Processo, end_vir: int):
    """
    Carrega uma página de um processo na memória física.
    Usa a política FIFO se a memória estiver cheia.
    """
    numero_pagina, _ = proc.tab_pags.traduzir_endereco_virtual(end_vir)
    
    if memo_fis.isFull():
        # Se a memória está cheia, usa FIFO para substituir
        frame = memo_fis.memoria[memo_fis.firstIn]
        frame.id_processo = proc.pid
        frame.id_pagina = numero_pagina
        frame.ocupado = True

        proc.tab_pags.tabela[numero_pagina] = frame
        memo_fis.firstIn = (memo_fis.firstIn + 1) % len(memo_fis.memoria)
    else:
        # Se há espaço livre, usa o primeiro frame disponível
        frame_livre = memo_fis.findLivre()
        if frame_livre:
            frame_livre.id_processo = proc.pid
            frame_livre.id_pagina = numero_pagina
            frame_livre.ocupado = True
            proc.tab_pags.tabela[numero_pagina] = frame_livre
        else:
            raise Exception("Não foi possível encontrar um frame livre")

# Exemplo de uso
"""
    # Inicializa a memória física
    mem_fisica = MemFis(tam_mem_fis, id_frm_ini, tam_frm)
    processos: Dict[int, Processo] = {}

    # Cria e carrega páginas para o processo 1
    processo1 = Processo(pid=1, tamanho=1024, tamanho_pagina=256)
    processos[1] = processo1
    carregarPag(mem_fisica, processo1, 0)    # Carrega a primeira página
    carregarPag(mem_fisica, processo1, 256)  # Carrega a segunda página

    # Cria e carrega páginas para o processo 2
    processo2 = Processo(pid=2, tamanho=512, tamanho_pagina=256)
    processos[2] = processo2
    carregarPag(mem_fisica, processo2, 0)    # Carrega a primeira página

    # Imprime o status atual da memória física
    print_status(mem_fisica)

    # Exemplo de acesso a dados
    try:
        dado = processo1.acessar_dados(100)
        print(f"Dado acessado pelo processo 1: {dado}")
    except Exception as e:
        print(f"Erro ao acessar dados: {e}")
"""