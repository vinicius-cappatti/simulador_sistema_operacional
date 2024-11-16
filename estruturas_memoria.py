from typing import List
from typing import Dict

class PageTable:
    def __init__(self, lista_frames: List[Frame]):
        self.lista_frames = lista_frames        # Frames armazenados na tabela de pagina

class Processo:
    def __init__(self, pid: int, tamanho: int, tab_pags: PageTable, mem_vir: List[int]):
        self.pid = pid                          # Identificador do processo
        self.tamanho = tamanho                  # Tamanho do processo
        self.tab_pags = tab_pags                # Tabela de paginas 
        self.memo_virtual = mem_vir             # Memoria virtual de cada processo