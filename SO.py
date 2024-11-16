# SO.py

import time
import random
from typing import List, Dict

from estruturas_memoria import Frame, MemFis, Processo

class SO:
    def __init__(self, tam_mem_fis: int, id_frame_initial: int, tam_frm: int):
        self.mem_fisica = MemFis(tam_mem_fis, id_frame_initial, tam_frm)
        self.processos: Dict[int, Processo] = {}

    def criar_processo(self, pid: int, tamanho: int, tamanho_pagina: int):
        processo = Processo(pid, tamanho, tamanho_pagina)
        self.processos[pid] = processo
        print(f"Processo {pid} criado com tamanho {tamanho} e tamanho de página {tamanho_pagina}")
        time.sleep(1)  # Simulando um atraso na criação do processo

    def carregar_pagina(self, pid: int, end_vir: int):
        processo = self.processos.get(pid)
        if not processo:
            print(f"Erro: Processo {pid} não existe")
            return

        numero_pagina, _ = processo.tab_pags.traduzir_endereco_virtual(end_vir)
    
        if numero_pagina >= processo.num_paginas:
            print(f"Erro: Número de página {numero_pagina} inválido para o processo {pid}")
            return

        print(f"Tentando carregar página {numero_pagina} do processo {pid}")
        time.sleep(1)  # Simulando tempo de processamento

        if self.mem_fisica.isFull():
            print(f"PAGEFAULT001: Memória física cheia")
            self.substituir_pagina(processo, numero_pagina)
        else:
            frame_livre = self.mem_fisica.findLivre()
            if frame_livre:
                self.carregar_pagina_em_frame(processo, numero_pagina, frame_livre)
            else:
                print(f"Erro: Não foi possível encontrar um frame livre")

    def substituir_pagina(self, processo: Processo, numero_pagina: int):
        print(f"Iniciando substituição de página aleatória")
        frame_aleatorio = random.choice(self.mem_fisica.memoria)
        print(f"Frame {frame_aleatorio.id} selecionado para substituição")
        
        # Simula o tempo de escrita da página substituída no disco
        time.sleep(2)
        print(f"Página do frame {frame_aleatorio.id} escrita no disco")

        self.carregar_pagina_em_frame(processo, numero_pagina, frame_aleatorio)

    def carregar_pagina_em_frame(self, processo: Processo, numero_pagina: int, frame: Frame):
        # Simula o tempo de leitura da página do disco
        time.sleep(2)
        print(f"Página {numero_pagina} do processo {processo.pid} carregada do disco")

        frame.ocupado = True
        frame.id_processo = processo.pid
        frame.id_pagina = numero_pagina
        
        if 0 <= numero_pagina < processo.tab_pags.num_paginas:
            processo.tab_pags.tabela[numero_pagina] = frame
            print(f"Página {numero_pagina} do processo {processo.pid} carregada no frame {frame.id}")
        else:
            print(f"Erro: Número de página {numero_pagina} inválido para o processo {processo.pid}")

    def acessar_memoria(self, pid: int, endereco: int):
        processo = self.processos.get(pid)
        if not processo:
            print(f"Erro: Processo {pid} não existe")
            return

        try:
            dado = processo.acessar_dados(endereco)
            print(f"Processo {pid} acessou o endereço {endereco}: {dado}")
        except Exception as e:
            print(f"Erro ao acessar memória: {e}")
            self.carregar_pagina(pid, endereco)

    def imprimir_estado_memoria(self):
        print(f"\nEstado atual da memória física:")
        for frame in self.mem_fisica.memoria:
            if frame.isOcupado():
                print(f"Frame {frame.id}: Processo {frame.id_processo}, Página {frame.id_pagina}")
            else:
                print(f"Frame {frame.id}: Livre")
        print()