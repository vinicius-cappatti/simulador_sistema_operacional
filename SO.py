# SO.py

import time
import random
from typing import List, Dict

from estruturas_memoria import Frame, MemFis, Processo, MemVir

class SO:
    """
    Representa um sistema operacional de uma máquina, contém a memória física e armazena processos em dicionário
    """
    def __init__(self, tam_mem_fis: int, id_frame_initial: int, tam_frm_pagina: int, inicio_memoria_virtual: int, qnt_paginas: int):
        self.mem_fisica = MemFis(tam_mem_fis, id_frame_initial, tam_frm_pagina)
        self.processos: Dict[int, Processo] = {}
        self.memoria_virtual = MemVir(inicio_memoria_virtual, qnt_paginas, tam_frm_pagina)

    # FUNÇÕES DE INICIALIZAÇÃO DE OBJETOS ------------------------------------------------------------------------------

    def criar_processo(self, pid: int, tamanho: int, tamanho_pagina: int, delay_padrao: int, caminho_logs: str):
        """Cria um processo novo com as especificações do parâmetro e armazena dentro do
        dicionario de processos do objeto"""
        self.processos[pid] = Processo(pid, tamanho, tamanho_pagina)
        with open(caminho_logs, "a", encoding= "utf-8") as arquivo_logs:
            arquivo_logs.write(f"Processo {pid} criado com tamanho {tamanho} e tamanho de página {tamanho_pagina}\n")
        time.sleep(delay_padrao)  # Simulando um atraso na criação do processo

    # FUNÇÕES DE ALOCAÇÃO DE VALORES -----------------------------------------------------------------------------------

    def alocar_procs_memoria_virtual(self):
        """Atribui um processo para cada página da memória virtual"""
        for indice_processo in self.processos:
            for i in range(self.processos[indice_processo].num_paginas):
                self.memoria_virtual.memoria[i].id_processo = indice_processo

    def alocar_pagina_memoria_fisica(self, processo: Processo, memoria_fisica: MemFis, id_pagina: int, delay_mem_sec: int, caminho_log: str):
        """Aloca uma página da memória virtual na memória física na memória virtual, por ser uma alocação vai """

        frame_livre = memoria_fisica.findLivre()
        indice_frame_livre = memoria_fisica.find_posicao_frame_livre()

        # FIFO: Se a memória está cheia a gente substitui o elemento que entrou primeiro
        if frame_livre == None:
            frame_livre = memoria_fisica.memoria[memoria_fisica.firstIn]
            indice_frame_livre = memoria_fisica.firstIn
            memoria_fisica.firstIn += 1                 # Atualiza a posição do elemento mais antigo
        
        frame_livre.ocupado = True
        frame_livre.id_processo = processo.pid
        frame_livre.id_pagina = id_pagina

        time.sleep(delay_mem_sec)

        memoria_fisica.memoria[indice_frame_livre] = frame_livre
        with open(caminho_log, "a", encoding="utf-8") as arquivo_logs:
            arquivo_logs.write(f"Frame {frame_livre.id} alocado para o processo {processo.pid} página f{id_pagina}")

    # FUNÇÕES DE ACESSO NA MEMÓRIA -------------------------------------------------------------------------------------

    def carregar_pagina(self, pid: int, end_vir: int, delay_acesso_mem_sec: int, caminho_logs: str):
        with open(caminho_logs, "a", encoding= "utf-8") as arquivo_logs:
            processo = self.processos.get(pid)
            if not processo:
                arquivo_logs.write(f"Erro: Processo {pid} não existe\n")
                return

            numero_pagina, _ = processo.tab_pags.traduzir_endereco_virtual(end_vir)
        
            if numero_pagina >= processo.num_paginas:
                arquivo_logs.write(f"Erro: Número de página {numero_pagina} inválido para o processo {pid}\n")
                return

            arquivo_logs.write(f"Tentando carregar página {numero_pagina} do processo {pid}\n")
            time.sleep(delay_acesso_mem_sec)  # Simulando tempo de processamento
    

            if self.mem_fisica.isFull():
                arquivo_logs.write(f"PAGEFAULT001: Memória física cheia\n")
                self.substituir_pagina(processo, numero_pagina)
            else:
                frame_livre = self.mem_fisica.findLivre()
                if frame_livre:
                    self.carregar_pagina_em_frame(processo, numero_pagina, frame_livre)
                else:
                    arquivo_logs.write(f"Erro: Não foi possível encontrar um frame livre\n")

    def substituir_pagina(self, processo: Processo, numero_pagina: int, delay_acesso_mem_sec: int):
        print(f"Iniciando substituição de página aleatória")
        frame_aleatorio = random.choice(self.mem_fisica.memoria)
        print(f"Frame {frame_aleatorio.id} selecionado para substituição")
        
        # Simula o tempo de escrita da página substituída no disco
        time.sleep(delay_acesso_mem_sec)
        print(f"Página do frame {frame_aleatorio.id} escrita no disco")

        self.carregar_pagina_em_frame(processo, numero_pagina, frame_aleatorio, delay_acesso_mem_sec)

    def acessar_memoria(self, pid: int, endereco: int, delay_acesso_mem_sec: int, caminho_logs: str):
        with open(caminho_logs, "a", encoding= "utf-8") as arquivo_logs:
            processo = self.processos.get(pid)
            if not processo:
                arquivo_logs.write(f"Erro: Processo {pid} não existe")
                return

            try:
                dado = processo.acessar_dados(endereco)
                arquivo_logs.write(f"Processo {pid} acessou o endereço {endereco}: {dado}")
            except Exception as e:
                arquivo_logs.write(f"Erro ao acessar memória: {e}")
                self.carregar_pagina(pid, endereco, delay_acesso_mem_sec, caminho_logs)

    def imprimir_estado_memoria(self, log_path: str):
        with open(log_path, "a", encoding="utf-8") as arquivo_logs:
            arquivo_logs.write(f"\nEstado atual da memória física:\n")
            for frame in self.mem_fisica.memoria:
                if frame.isOcupado():
                    arquivo_logs.write(f"\nFrame {frame.id}: Processo {frame.id_processo}, Página {frame.id_pagina}")
                else:
                    arquivo_logs.write(f"\nFrame {frame.id}: Livre")
            arquivo_logs.write("\n")