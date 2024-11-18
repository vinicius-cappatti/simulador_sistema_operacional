from utils import ler_config
from SO import SO
import random
import sys

# Leitura dos parâmetros do programa
if len(sys.argv) > 1:
    arquivo_entrada = sys.argv[1]
else:
    arquivo_entrada = "entrada.csv"
config = ler_config(arquivo_entrada)

memoria_real = int(config['Memoria Real'])                                          # Define o tamanho da memória física em nro de frames
memoria_virtual = int(config['Memoria Virtual'])                                    # Define o tamanho da memória virtual em nro de paginas
numero_processos = int(config['Processos'])                                         # Define o numero de processos rodando
qnt_paginas_processo = int(config['Quantidade de paginas por processo'])            # Número de páginas que cada processo tem
tamanho_frame_pagina = int(config['Tam. Frame/Pagina'])                             # Quantos endereços tem dentro de cada página
frame_inicial = int(config['Frame Inicial'])                                        # Endereço do primeiro frame na memória física
pagina_inicial_virtual = int(config['Pagina Inicial Virtual'])                      # Endereço da primeira página na memória virtual
delay_operacao_normal = int(config['Delay Operacao Normal'])                        # Parâmetro de sleep operações normais
delay_acesso_memoria_secundaria = int(config['Delay Acesso Memoria Secundaria'])    # Sleep ao acessar memória secundária
caminho_logs = config['Caminho Logs']                                               # Arquivo onde ficam os logs
limite_iteracoes = int(config['Limite de iteracoes'])                               # Define quantos acessos na memória serão feitos

frame_final = frame_inicial + memoria_real * tamanho_frame_pagina                   # Define o endereço do último frame da memória física
pagina_final = pagina_inicial_virtual + memoria_virtual * tamanho_frame_pagina      # Define o endereço da última página na memória virtual

with open(caminho_logs, "w") as arquivo_logs:
    arquivo_logs.write("")                                                          # Apaga o conteudo do arquivo caso ele ja existisse

def main():

    # Inicializa o SO com as configurações de 
    sistema_operacional = SO(tam_mem_fis=memoria_real, 
                             id_frame_initial=frame_inicial, 
                             tam_frm_pagina=tamanho_frame_pagina,
                             inicio_memoria_virtual= pagina_inicial_virtual)

    # Cria alguns processos
    endereco_pagina_criada = 1
    for i in range(numero_processos):
        # Função criar_processo armazena em uma lista de processos dentro do objeto SO
        sistema_operacional.criar_processo(pid= i + 1, 
                                           paginas_por_processo= qnt_paginas_processo, 
                                           tamanho_pagina= tamanho_frame_pagina, 
                                           delay_padrao= delay_operacao_normal,
                                           endereco_pagina_criada = endereco_pagina_criada,
                                           caminho_logs= caminho_logs)
        endereco_pagina_criada += qnt_paginas_processo

    for acesso in range(limite_iteracoes + 1):
        sistema_operacional.imprimir_estado_memoria(caminho_logs)
        # 1. Selecionar um processo aleatório
        pid_processo_atual = random.randint(1, numero_processos)
        # 2. Calcular um endereço virtual aleatório que aquele processo pode acessar
        endereco_minimo = pagina_inicial_virtual + tamanho_frame_pagina * qnt_paginas_processo * (pid_processo_atual - 1) + (qnt_paginas_processo * (pid_processo_atual - 1) - 1)
        if pid_processo_atual == 1:
            endereco_minimo = pagina_inicial_virtual # Condição pq essa fórmula é muito chata
        endereco_maximo = pagina_inicial_virtual + tamanho_frame_pagina * qnt_paginas_processo * pid_processo_atual + (qnt_paginas_processo * pid_processo_atual - 2)

        endereco_atual = random.randint(endereco_minimo, endereco_maximo)
        # 3. Calcular qual a página da memória virtual está sendo acessada
        pagina_memoria_virtual_acessada = sistema_operacional.traduz_endereco_para_pagina(endereco_atual, pagina_inicial_virtual)

        # 4. Acessar memória física
        sistema_operacional.acessar_memoria(pid_processo_atual, 
                                            pagina_memoria_virtual_acessada, 
                                            delay_operacao_normal,
                                            delay_acesso_memoria_secundaria,
                                            caminho_logs)

        #Implementação da pausa
        print(f"Acesso {acesso + 1}/{limite_iteracoes}")
        opcao = input("Operação pausada, selecione uma opção:\n1. [a]bortar\n2. [c]ontinuar\nescolha sua opção: ").lower().replace(" ", "")
        while opcao != "a" and opcao != "c":
            opcao = input("Selecione uma opção válida [a/c]:").lower().replace(" ", "")
        
        if(opcao == "a"):
            return

if __name__ == "__main__":
    main()
