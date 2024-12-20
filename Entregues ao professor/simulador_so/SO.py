# SO.py

import time
import random
from typing import List, Dict

from estruturas_memoria import MemFis, Processo

class SO:
    """
    Representa um sistema operacional de uma máquina, contém a memória física e armazena processos em dicionário
    """
    def __init__(self, tam_mem_fis: int, id_frame_initial: int, tam_frm_pagina: int, inicio_memoria_virtual: int):
        self.mem_fisica = MemFis(tam_mem_fis, id_frame_initial, tam_frm_pagina)
        self.processos: Dict[int, Processo] = {}
        self.end_virtual_inicial = inicio_memoria_virtual
        self.memoria_virtual:  Dict[int, Processo] = {}
        self.tam_pagina_frames = tam_frm_pagina

    # FUNÇÕES DE INICIALIZAÇÃO DE OBJETOS ------------------------------------------------------------------------------

    def criar_processo(self, pid: int, paginas_por_processo: int, tamanho_pagina: int, endereco_pagina_criada: int,
                       delay_padrao: int, caminho_logs: str):
        """Cria um processo novo com as especificações do parâmetro e armazena dentro do
        dicionario de processos do objeto"""
        self.processos[pid] = Processo(pid, paginas_por_processo, tamanho_pagina, endereco_pagina_criada)
        with open(caminho_logs, "a", encoding= "utf-8") as arquivo_logs:
            arquivo_logs.write(f"\n\nProcesso {pid} criado com tamanho {paginas_por_processo} e tamanho de página {tamanho_pagina}")
        time.sleep(delay_padrao)  # Simulando um atraso na criação do processo

    def inicializar_memoria_virtual(self, qnt_paginas_processo: int, qnt_processos: int, memoria_virtual: int, caminho_logs: str):
        if qnt_paginas_processo * qnt_processos > memoria_virtual:
            with open(caminho_logs, "a", encoding="utf-8") as arquivo_logs:
                arquivo_logs.write(f"ABORTAR: O número de páginas criadas deve ser menor ou igual ao tamanho da memória virtual!!!\n")
            return False
        
        for i in range(memoria_virtual):
            self.memoria_virtual[i] = None
        
        with open(caminho_logs, "a", encoding="utf-8") as arquivo_logs:
                arquivo_logs.write(f"Memória virtual inicializada com sucesso\n")
        
        return True

    def alocar_processo_memoria_virtual(self, pid: int, qnt_paginas_processo: int, endereco_inicial: int, delay_mem_sec: int,  caminho_logs: str):
        
        time.sleep(delay_mem_sec)

        for i in range(qnt_paginas_processo):
            self.memoria_virtual[endereco_inicial + i - 1] = self.processos.get(pid)
            with open(caminho_logs, "a", encoding="utf-8") as arquivo_logs:
                arquivo_logs.write(f"\nProcesso {pid} alocado no endereço {endereco_inicial + i} da memória virtual")
            
    # FUNÇÕES DE ACESSO NA MEMÓRIA -------------------------------------------------------------------------------------

    def acessar_memoria(self, pid: int, pagina_acessada: int, endereco: int, delay_normal: int, delay_acesso_mem_sec: int, caminho_logs: str):
        """
        ARGS:
        * pid: endereço do processo que está tentando acessar a memória
        * pagina_acessada: endereço da página na memória virtual
        * endereco: é o endereço atual que o processo quer acessar
        * delay_normal: tempo de acesso à memória física
        * delay_acesso_mem_sec: tempo de acesso à memória secundária / virtual
        * caminho_logs: caminho para o arquivo de logs
        """
        with open(caminho_logs, "a", encoding= "utf-8") as arquivo_logs:
            arquivo_logs.write(f"\nProcesso {pid} está tentando acessar o endereço {endereco} da página {pagina_acessada}")

            processo = self.processos.get(pid)
            frame = processo.tab_pags.tabela[pagina_acessada]

            if frame != None and frame != -1:
                time.sleep(delay_normal)
                arquivo_logs.write(f"\nProcesso {pid} acessou o frame {frame.id} que contém a página {frame.id_pagina}")
                return

            arquivo_logs.write(f"\n[PAGE FAULT] Página {pagina_acessada} não está na memória física")
            time.sleep(delay_acesso_mem_sec)

            frame = self.mem_fisica.findLivre()

            if frame == None:
                frame = self.mem_fisica.memoria[self.mem_fisica.firstIn]
                self.mem_fisica.aumenta_first_in()
                # Atualizar a tabela de páginas do processo quando removemos a página dele no FIFO
                # Remove referência ao frame na tabela de páginas antiga
                self.processos.get(frame.id_processo).tab_pags.tabela[frame.id_pagina] = None 
                
            
            pos_frame = self.mem_fisica.find_posicao_frame(frame)

            frame.ocupado = True
            frame.id_processo = processo.pid
            frame.id_pagina = pagina_acessada

            self.mem_fisica.memoria[pos_frame] = frame
            processo.tab_pags.tabela[pagina_acessada] = frame
            arquivo_logs.write(f"\nFrame {frame.id} atualizado com sucesso!!! Agora ele contém a página {pagina_acessada}")


# FUNÇÃO DE MAPEAMENTO -------------------------------------------------------------------------------------
  
    def encontra_pagina_processo_na_memoria_virtual(self, pagina_do_processo: int, processo: Processo):
        for pagina in self.memoria_virtual.memoria:
            if pagina.id_processo == processo.pid and pagina.nro_pagina_no_processo == pagina_do_processo:
                return pagina.endereco
        return None
    
    def traduz_endereco_para_pagina(self, endereco: int, endereco_inicial: int):
        resultado = (endereco - endereco_inicial) % self.tam_pagina_frames
        if resultado == 0:
            return ((endereco - endereco_inicial) // self.tam_pagina_frames)
        else:
            return ((endereco - endereco_inicial) // self.tam_pagina_frames) + 1

# FUNÇÃO DE IMPRESSÃO DE LOG -------------------------------------------------------------------------------------

    def imprimir_estado_memoria(self, log_path: str):
        with open(log_path, "a", encoding="utf-8") as arquivo_logs:
            arquivo_logs.write(f"\n\nEstado atual da memória física:\n")
            for frame in self.mem_fisica.memoria:
                if frame.isOcupado():
                    arquivo_logs.write(f"\nFrame {frame.id}: Processo {frame.id_processo}, Página {frame.id_pagina}")
                else:
                    arquivo_logs.write(f"\nFrame {frame.id}: Livre")
            arquivo_logs.write(f"\nFrame mais antigo é {self.mem_fisica.firstIn}\n")
    
    def imprimir_memoria_virtual(self, log_path: str):
        with open(log_path, "a", encoding="utf-8") as arquivo_log:
            arquivo_log.write("\n\nEstado inicial da memoria virtual:")
            for endereco in self.memoria_virtual:
                if self.memoria_virtual[endereco] == None:
                    arquivo_log.write(f"\nPágina {endereco + 1}: Livre")
                else:
                    arquivo_log.write(f"\nPágina {endereco + 1}: Processo {self.memoria_virtual[endereco].pid}")
