from typing import List
from typing import Dict

class Frame:
    def __init__(self, id: int, ocupado: bool, id_processo: int, id_pagina: int):
        self.id = id                            # Endereco do frame na memoria fisica
        self.ocupado = ocupado                  # Indica se esse frame esta vazio ou nao
        self.id_processo = id_processo          # Se ocupado = True, indica qual processo ocupa o Frame
        self.id_pagina = id_pagina              # Se ocupado = True, indica qual pagina ocupa o Frame
class PageTable:
    def __init__(self, tab: Dict[int, Frame]):
        self.tab = tab                          # Dicionario onde a chave é um inteiro com o número da página e o valor é um frame

class Pagina:
    def __init__(self, id: int, end_ini: int, dados: str):
        self.id = id                            # ID identificador da pagina
        self.end_ini = end_ini                  # Endereco inicial da pagina, o final sera obtido por inicial + tamanho (definido no processo)
        self.dados = dados                      # Dados dessa pagina
class Processo:
    def __init__(self, pid: int, num_pgs: int, tam_pgs: int, tab_pags: PageTable, mem_vir: List[int]):
        self.pid = pid                          # Identificador do processo
        self.num_pgs = num_pgs                  # Tamanho do processo
        self.tam_pgs = tam_pgs                  # Tamanho de uma pagina
        self.tab_pags = tab_pags                # Tabela de paginas
        self.memo_virtual = mem_vir             # Memoria virtual de cada processo

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

    def findLivre(self):
        for frm in self.memoria:
            if(frm.id_processo == None):
                return frm
        return None             # Se retorna None, a memoria fisica esta cheia
    
    def print_status(self):
        for frame in self.memoria:
            if(frame.isOcupado()):
                print(f"Processo: {frame.id_processo} Pagina: {frame.id_pagina}")
            else:
                print("----")