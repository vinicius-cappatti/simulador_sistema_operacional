from typing import Dict, List

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
    def __init__(self, num_paginas: int, tamanho_pagina: int, pagina_inicial: int):
        # Inicializa a tabela com None para cada página
        self.tabela: Dict[int, Frame] = {}
        for i in range(num_paginas):
            self.tabela[pagina_inicial + i] = None
        self.tamanho_pagina = tamanho_pagina
        self.num_paginas = num_paginas

class Processo:
    """
    Representa um processo no sistema.
    """
    def __init__(self, pid: int, num_paginas: int, tamanho_pagina: int, pagina_inicial: int):
        self.pid = pid
        self.num_paginas = num_paginas
        self.tab_pags = PageTable(self.num_paginas, tamanho_pagina, pagina_inicial)
        self.memo_virtual = list(range(num_paginas))

class MemFis:
    """
    Representa a memória física do sistema.
    """
    def __init__(self, tam_mem_fis: int, id_frame_initial: int, tam_frm: int):
        self.memoria: List[Frame] = [Frame(id_frame_initial + i * tam_frm) for i in range(tam_mem_fis)]
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
    
    def find_posicao_frame(self, frame_procurado: Frame) -> int:
        """Encontra a posição do primeiro frame procurado na memória física. Retorna None se não encontra"""
        for i in range(len(self.memoria)):
            if self.memoria[i] == frame_procurado:
                return i
        return None
    
    def aumenta_first_in(self):
        self.firstIn = (self.firstIn + 1) % len(self.memoria)