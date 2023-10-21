from BCP import BCP

# Inicialização das listas
prontos = []
bloqueados = []
tabela_de_processos = []

# Classe BCP (Blocos de Controle de Processo) continua a mesma

# Classe Escalonador
def log(message):
    with open("logXX.txt", "a") as log_file:
        log_file.write(message + "\n")

class Escalonador:
    def __init__(self, tabela_de_processos, pronto, bloqueado, quantum):
        self.tabela_de_processos = tabela_de_processos
        self.lista_pronto = pronto
        self.lista_bloqueado = bloqueado
        self.quantum = quantum

    def decrementa_espera_bloqueados(self):
        for processo_bloqueado in self.lista_bloqueado:
            processo_bloqueado.decrementa_espera()

        self.lista_bloqueado = [proc for proc in self.lista_bloqueado if proc.tempo_de_espera > 0]

    def run(self):
        while self.lista_pronto or self.lista_bloqueado:
            if self.lista_pronto:
                processo_atual = self.lista_pronto.pop(0)
                log(f"Executando {processo_atual.process_name}")

                # Execução do processo com um quantum limitado
                for _ in range(self.quantum):
                    if processo_atual.program_counter < len(processo_atual.instrucoes):
                        instrucao = processo_atual.instrucoes[processo_atual.program_counter]
                        processo_atual.incrementa_pc()

                        if instrucao == "E/S":
                            # Inicia uma operação de E/S e move o processo para a lista de bloqueados
                            processo_atual.tempo_de_espera = 5
                            self.lista_bloqueado.append(processo_atual)
                            log(f"E/S iniciada em {processo_atual.process_name}")
                            break
                        elif instrucao == "COM":
                            # Instrução de cálculo/computação
                            pass
                        elif instrucao == "SAIDA":
                            # Processo concluído; remove-o da lista de prontos e registra os valores dos registradores
                            self.lista_pronto.remove(processo_atual)
                            log(f"{processo_atual.process_name} terminado. X={processo_atual.register1}. Y={processo_atual.register2}")
                            break
                        else:
                            registrador, valor = instrucao.split("=")
                            if registrador == "X":
                                processo_atual.register1 = int(valor)
                            else:
                                processo_atual.register2 = int(valor)

                log(f"Interrompendo {processo_atual.process_name} após {self.quantum} instruções")
                self.decrementa_espera_bloqueados()

# Carrega os processos a partir de arquivos de texto
def carrega_arquivos():
    for i in range(1, 12):
        nome_arquivo = f"programas/{i:02}.txt"
        with open(nome_arquivo, "r") as file:
            linhas = file.readlines()
            process_name = linhas[0].strip()
            instrucoes = [linha.strip() for linha in linhas[1:-1]]
            novo_processo = BCP(process_name, instrucoes, 0, None, None)
            tabela_de_processos.append(novo_processo)
            prontos.append(novo_processo)

# Carregando processos a partir dos arquivos
carrega_arquivos()

# Lendo o valor do quantum do arquivo "quantum.txt"
with open("quantum.txt", "r") as quantum_file:
    quantum = int(quantum_file.read())

# Inicializa escalonador com o valor do quantum e as listas de processos
escalonador = Escalonador(tabela_de_processos, prontos, bloqueados, quantum)

# Inicie o escalonador
escalonador.run()
