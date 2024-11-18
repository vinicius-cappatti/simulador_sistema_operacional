# projeto2So

## Descrição do projeto

O objetivo desse projeto é desenvolver um simulador simples do funcionamento de um sistema operacional utilizando a linguagem Python. Os parâmetros do sistema são definidos pelo usuário a partir de um arquivo passado no terminal, se o usuário não passar nenhum arquivo, usamos o padrão "entrada.csv" para buscar os dados de entrada.

O arquivo "entrada.csv" está junto deste README e deve ser usado como template caso queira mudar o arquivo de entrada.

## Estrutura do simulador

O simulador possui os objetos 
* **Frame:** representa uma subdivisão da memória física
* **Processo:** representa um processo rodando na máquina, é administrado pelo sistema operacional e alocado na memória virtual
* **PageTable:**  representa uma tabela de páginas, cada processo possui a sua e é quem faz o mapeamento da página na memória visual para frame na memória física
* **MemFis:** representa a memória física da máquina, sendo basicamente uma lista de Frames

Todos os objetos acima são administrados pelo objeto **SO** que representa o sistema operacional da máquina, é ele quem executa todas as operações de alocação e mapeamento durante a execução.

Durante a execução, o programa seleciona aleatóriamente um processo e um endereço virtual para que ele acesse, representando a execução do processo para acessar um dado, a partir disso o sistema operacional fica responsável por mapear se a página daquele endereço está na memória física ou não.

## Testes

Os arquivos com logs dos testes realizados estão armazenados na pasta /logs_testes mas seguem prints da execução:

**Valores de entrada**

![image](https://github.com/user-attachments/assets/4810bb27-ed04-42be-b14f-275de5af7ae2)

**Logs de execução**

![image](https://github.com/user-attachments/assets/6cbd1d40-c356-4ea1-b5bc-82559cf68b8c)

![image](https://github.com/user-attachments/assets/15e412f3-7508-46bd-a127-eb721980dc34)

![image](https://github.com/user-attachments/assets/be2c366a-2705-4482-a7ac-bfe32d350799)

![image](https://github.com/user-attachments/assets/df94de7d-93e4-4745-84be-f1f218fb9f27)

![image](https://github.com/user-attachments/assets/2ec70298-9d56-484d-b679-147ca04e20d3)

![image](https://github.com/user-attachments/assets/da7ea34c-521e-4772-a4fc-92ecc992f302)
