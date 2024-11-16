import estruturas_memoria as em
from typing import List

# Leitura dos parametros do programa
input_path = "entrada.csv"
param = f.ler_parametros(input_path)

tam_mem_fis = int(param[0])     # Define o tamanho da memoria fisica
tam_mem_vir = int(param[1])     # Define o tamanho da memoria virtual
tam_frm = int(param[2])         # Define o tamanho de um frame
num_proc = int(param[3])        # Define o numero de processos rodando
tam_procs = int(param[4])       # Define o tamanho dos processos e o numero de paginas de cada processo
id_frame_ini = int(param[5])    # Define o endereco do frame inicial da memoria fisica
id_pag_ini = int(param[6])      # Define o endereco da pagina inicial da memoria virtual 
logs_path = param[7]            # Define o caminho para o arquivo de saida dos logs
sleep_param = int(param[8])     # Define o tempo de dormencia de cada operacao que envolve acesso na memoria em ms

# Inicializacao da memoria fisica
memo_fis = em.MemFis(tam_mem_fis= tam_mem_fis, id_frm_ini= id_frame_ini, tam_frm= tam_frm)


# Inicializar os processos em uma lista
processos: List[f.Processo] = []
for i in range(num_proc):
    tp = em.PageTable(lista_frames= [])
    for c in range(tam_procs):
        tp.lista_frames.append(None) # Insere dados vazios na tabela de paginas do processo
    prAtual = em.Processo(pid = i, tamanho= tam_procs, tab_pags= tp)
    processos.append(prAtual)
print("Processos inicializados com sucesso")

print("\n=-=-=-=-=-=-=-=-=-=-=-=\n")

print("STATUS INICIAL DA MEMORIA FISICA")
memo_fis.printStatus()

for pg in range(tam_procs):
    for proc in processos:
        ex = proc.tab_pags.existe(pg)

        if(ex):
            print(f"A pagina {pg} do processo {proc.pid} esta na memoria fisica")
        else:
            print(f"[PAGE FAULT]")
