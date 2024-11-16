from typing import List
from typing import Dict

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
    
    def printStatus(self):
        """Imprime o status atual da memória física"""
        for frame in self.memoria:
            if frame.isOcupado():
                print(f"P{frame.id_processo} -> pg. {frame.id_pagina}")
            else:
                print("---")