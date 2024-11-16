import csv
from typing import List, Dict
import estruturas_memoria as em

def carregarPag(memo_fis: em.MemFis, proc: em.Processo, end_vir: int):
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
