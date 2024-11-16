from funcoes import ler_config
from SO import SO
import random

# Leitura dos parâmetros do programa
arquivo_entrada = "entrada.csv"
config = ler_config(arquivo_entrada)
memoria_real = int(config['Memoria Real'])                                          # Define o tamanho da memória física em nro de frames
memoria_virtual = int(config['Memoria Virtual'])                                    # Define o tamanho da memória virtual em nro de paginas
numero_processos = int(config['Processos'])                                         # Define o numero de processos rodando
tamanho_processo = int(config['Tam. Processo'])                                     # Número de endereços acessados
tamanho_frame_pagina = int(config['Tam. Frame/Pagina'])                             # Quantos endereços tem dentro de cada página
frame_inicial = int(config['Frame Inicial'])                                        # Endereço do primeiro frame na memória física
pagina_inicial_virtual = int(config['Pagina Inicial Virtual'])                      # Endereço da primeira página na memória virtual
delay_operacao_normal = int(config['Delay Operacao Normal'])                        # Parâmetro de sleep operações normais
delay_acesso_memoria_secundaria = int(config['Delay Acesso Memoria Secundaria'])    # Sleep ao acessar memória secundária
caminho_logs = config['Caminho Logs']                                               # Arquivo onde ficam os logs

frame_final = frame_inicial + memoria_real * tamanho_frame_pagina                   # Define o endereço do último frame da memória física
pagina_final = pagina_inicial_virtual + memoria_virtual * tamanho_frame_pagina      # Define o endereço da última página na memória virtual
qnt_paginas_memoria = (tamanho_processo + tamanho_frame_pagina - 1) // tamanho_frame_pagina # Define o numero de páginas na memória virtual

with open(caminho_logs, "w") as arquivo_logs:
    arquivo_logs.write("")                                                          # Apaga o conteudo do arquivo caso ele ja existisse

def main():
    # Inicializa o SO com a configuração especificada
    sistema_operacional = SO(tam_mem_fis=memoria_real, 
                             id_frame_initial=frame_inicial, 
                             tam_frm_pagina=tamanho_frame_pagina,
                             inicio_memoria_virtual= pagina_inicial_virtual,
                             qnt_paginas= qnt_paginas_memoria)

    # Cria alguns processos
    for i in range(numero_processos):
        # Função criar_processo armazena em uma lista de processos dentro do objeto SO
        sistema_operacional.criar_processo(pid= i + 1, 
                                           tamanho= tamanho_processo, 
                                           tamanho_pagina= tamanho_frame_pagina, 
                                           delay_padrao= delay_operacao_normal,
                                           caminho_logs= caminho_logs)

    sistema_operacional.alocar_procs_memoria_virtual()  # Atribui os processos da lista interna de processos às páginas da memória virtual

    sistema_operacional.imprimir_estado_memoria(caminho_logs)

if __name__ == "__main__":
    main()
