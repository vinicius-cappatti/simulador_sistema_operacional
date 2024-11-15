"""
AUTORES
* Thomaz S. Scopel
* Vinicius S. Cappatti - 10418266

ARQUIVO: Esse arquivo contem as funcoes e as classes utilizadas no projeto
"""
import csv
from typing import List

class Frame:
    def __init__(self, id: int, ocupado: bool, id_processo: int, id_pagina: int):
        self.id = id                            # Endereco do frame na memoria fisica
        self.ocupado = ocupado                  # Indica se esse frame esta vazio ou nao
        self.id_processo = id_processo          # Se ocupado = True, indica qual processo ocupa o Frame
        self.id_pagina = id_pagina              # Se ocupado = True, indica qual pagina ocupa o Frame

    def isOcupado(self):
        return self.ocupado

class Pagina:
    def __init__(self, id: int, alocada_mem_fis: bool):
        self.id = id                            # ID identificador da pagina
        self.alocada_mem_fis = alocada_mem_fis  # Indica se a pagina em questao esta alocada na memoria fisica

def ler_parametros(caminho_csv):
    with open(caminho_csv, mode='r', encoding='utf-8') as arquivo:
        leitor = csv.reader(arquivo, delimiter= ";")
        next(leitor, None)  # Ignora a primeira linha pois ela contem o cabecalho
        parametros = next(leitor, None)  # Le somente a segunda linha que contem os parametros
        return parametros

class PageTable:
    """
    Cada tabela de paginas eh uma lista de frames, onde a posicao desse frame na lista 
    representa o endereco da pagina ao qual ele esta associado
    """
    def __init__(self, lista_frames: List[Frame]):
        self.lista_frames = lista_frames        # Frames armazenados na tabela de pagina
    
    def traduzir_endereco_virtual(self, end_vir: int):
        if(end_vir < 0 or end_vir > len(self.lista_frames)):
            return False

        return self.lista_frames[end_vir].id
    
    def armazena(self, pro: 'Processo', dado: str, end_vir: int):
        if(end_vir < 0 or end_vir > len(self.lista_frames)):
            return Exception

        frame = self.lista_frames[end_vir]

        frame.ocupado = True
        frame.id_processo = pro.pid
        frame.id_pagina = end_vir
        frame.dados = dado

        self.lista_frames[end_vir] = frame
    
    def existe(self, end_vir: int):
        if( end_vir < 0 or end_vir > len(self.lista_frames) or self.lista_frames[end_vir] == None):
            return False
        else:
            return True

class Processo:
    def __init__(self, pid: int, tamanho: int, tab_pags: PageTable):
        self.pid = pid                          # Identificador do processo
        self.tamanho = tamanho                  # Tamanho do processo
        self.tab_pags = tab_pags                # Tabela de paginas 
    
    def acessar_dados(self, endereco_acessado: int):
        if(endereco_acessado < 0 or endereco_acessado >= len(self.tab_pags.lista_frames)):
            print(f"Tentativa de acesso a endereco invalido. Processo {self.pid} e endereco {endereco_acessado}")
            return Exception

        frame = self.tab_pags.lista_frames[endereco_acessado]

        if(not frame.isOcupado()):
            print(f"Tentativa de se ocupar frame desocupado. Processo {self.pid} endereco {endereco_acessado}")
            return Exception

        if(frame.id_processo != self.pid):
            print(f"Tentativa do processo {self.pid} acessar frame ocupado pelo processo {frame.id_processo}")
            return Exception

        return frame.dados

class MemFis:
    def __init__(self, tam_mem_fis: int, id_frm_ini: int, tam_frm: int):
        self.firstIn = 0
        self.memoria: List[Frame] = []

        for n in range(tam_mem_fis):
            fAtual = Frame(id= id_frm_ini + n * tam_frm, ocupado= False, id_processo= None, id_pagina= None)
            self.memoria.append(fAtual)
    
    def isFull(self):
        for frm in self.memoria:
            if(frm.id_processo == None):
                return False
        return True

    def find

def print_status(memo_fis: List[Frame]):
    for frame in memo_fis:
        if(frame.isOcupado()):
            print(f"Processo: {frame.id_processo} Pagina: {frame.id_pagina}")
        else:
            print("----")

def carregarPag(memo_fis: MemFis, proc: Processo, ende: int):
    if(memo_fis.isFull()):
        frame = memo_fis.memoria[memo_fis.firstIn]
        frame.id_processo = proc.pid
        frame.id_pagina = ende

        proc.tab_pags[ende] = frame
        memo_fis.memoria[memo_fis.firstIn] = frame

        memo_fis.firstIn += 1
    else:
        