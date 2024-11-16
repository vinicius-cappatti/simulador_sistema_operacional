from utils import ler_config
from SO import SO
import random

# Leitura dos parâmetros do programa
arquivo_entrada = "entrada.csv"
config = ler_config(arquivo_entrada)
memoria_real = int(config['Memoria Real'])                                      # Define o tamanho da memória física
memoria_virtual = int(config['Memoria Virtual'])                                # Define o tamanho da memória virtual
numero_processos = int(config['Processos'])
tamanho_processo = int(config['Tam. Processo'])
tamanho_frame_pagina = int(config['Tam. Frame/Pagina'])
pagina_inicial_real = int(config['Pagina Inicial Real'])
pagina_inicial_virtual = int(config['Pagina Inicial Virtual'])
delay_operacao_normal = int(config['Delay Operacao Normal'])
delay_acesso_memoria_secundaria = int(config['Delay Acesso Memoria Secundaria'])
caminho_logs = config['Caminho Logs']

def main():
    # Inicializa o SO com a configuração especificada
    sistema_operacional = SO(tam_mem_fis=memoria_real, 
                             id_frame_initial=pagina_inicial_real, 
                             tam_frm=tamanho_frame_pagina)

    # Cria alguns processos
    sistema_operacional.criar_processo(pid=1, tamanho=tamanho_processo, tamanho_pagina=tamanho_frame_pagina)
    sistema_operacional.criar_processo(pid=2, tamanho=tamanho_processo, tamanho_pagina=tamanho_frame_pagina)
    sistema_operacional.criar_processo(pid=3, tamanho=tamanho_processo, tamanho_pagina=tamanho_frame_pagina)

    # Simula algumas operações de acesso à memória
    for _ in range(20):
        pid_aleatorio = random.choice([1, 2, 3])
        endereco_aleatorio = random.randint(0, 1023)  # Endereço aleatório até 1023
        sistema_operacional.acessar_memoria(pid_aleatorio, endereco_aleatorio)
        sistema_operacional.imprimir_estado_memoria()

    sistema_operacional.imprimir_estado_memoria()

if __name__ == "__main__":
    main()