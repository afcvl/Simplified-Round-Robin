from BCP import BCP

def log(message):
    with open("logXX.txt", "a") as log_file:
        log_file.write(message + "\n")
        
def clear_log(path):
    with open(path, "w") as log_file:
        log_file.write("")
        
# Inicialização das listas

prontos = []

bloqueados = []

tabela_de_processos = []

# Classe Escalonador
class Escalonador:
    def __init__(self, tabela_de_processos, pronto, bloqueado, quantum):
        self.tabela_de_processos = tabela_de_processos
        self.lista_pronto = pronto
        self.lista_bloqueado = bloqueado
        self.quantum = quantum
    
    def decrementa_espera_bloqueados(self):
        
        i = 0
        
        processos_liberados = []
        
        while i < len(self.lista_bloqueado):  # decremento do tempo dos bloqueados
            
            processo_bloqueado = self.lista_bloqueado[i]
            processo_bloqueado.decrementa_espera()
            
            if processo_bloqueado.tempo_de_espera <= 0:
                processos_liberados.append(i)
                
            i += 1
            
        for i in list(reversed(processos_liberados)):  # liberacão dos processos prontos
            self.lista_pronto.insert(len(self.lista_pronto), self.lista_bloqueado.pop(i))           

    def run(self):
        trocas_de_contexto = 0
        
        media_instrucoes = []
        
        while self.lista_pronto or self.lista_bloqueado:
            
            if self.lista_pronto:
                processo_atual = self.lista_pronto.pop(0)
                
                log(f"Executando {processo_atual.process_name}")

                # Execução do processo com um quantum limitado
                n_comp = 0
                for n_quantum in range(1, self.quantum + 1):
                    if processo_atual.program_counter < len(processo_atual.instrucoes):
                        instrucao = processo_atual.instrucoes[processo_atual.program_counter]
                        processo_atual.incrementa_pc()

                        self.decrementa_espera_bloqueados()
                        
                        if instrucao == "E/S":
                            # Inicia uma operação de E/S e move o processo para a lista de bloqueados
                            processo_atual.tempo_de_espera = 10
                            self.lista_bloqueado.insert(len(self.lista_bloqueado), processo_atual)
                            log(f"E/S iniciada em {processo_atual.process_name}")
                            trocas_de_contexto += 1
                            break
                        
                        elif instrucao == "COM":
                            # Instrução de cálculo/computação
                            n_comp += 1
                            pass
                        
                        elif instrucao == "SAIDA":
                            # Processo concluído; remove-o da lista de prontos e registra os valores dos registradores
                            log(f"{processo_atual.process_name} terminado. X={processo_atual.register1}. Y={processo_atual.register2}")
                            trocas_de_contexto += 1
                            break
                        
                        else:
                            registrador, valor = instrucao.split("=")
                            if registrador == "X":
                                processo_atual.register1 = int(valor)
                            else:
                                processo_atual.register2 = int(valor)
                            n_comp += 1

                media_instrucoes.append(n_comp)
                
                # caso não ocorra impedimentos para rodar o processo
                if n_comp == self.quantum:
                    self.lista_pronto.insert(len(self.lista_pronto), processo_atual)
                    trocas_de_contexto += 1

                log(f"Interrompendo {processo_atual.process_name} após {n_quantum} instruções")
                
            else:
                self.decrementa_espera_bloqueados()
                
        log(f"MEDIA DE TROCAS: {trocas_de_contexto/10}")
        log(f"MEDIA DE INSTRUCOES POR USO DE CPU: {sum(media_instrucoes)/len(media_instrucoes):.2f}")
        log(f"QUANTUM: {self.quantum}")

# Carrega os processos a partir de arquivos de texto
def carrega_arquivos():
    for i in range(1, 11):
        nome_arquivo = f"programas/{i:02}.txt"
        with open(nome_arquivo, "r") as file:
            linhas = file.readlines()
            process_name = linhas[0].strip()
            instrucoes = [linha.strip() for linha in linhas[1:]]
            novo_processo = BCP(process_name, instrucoes, 0, None, None)
            tabela_de_processos.append(novo_processo)
            prontos.append(novo_processo)
            log(f"Carregando {process_name}")

# Carregando processos a partir dos arquivos
carrega_arquivos()

# Lendo o valor do quantum do arquivo "quantum.txt"
with open("programas/quantum.txt", "r") as quantum_file:
    quantum = int(quantum_file.read())
    
clear_log("logXX.txt")

# Inicializa escalonador com o valor do quantum e as listas de processos
escalonador = Escalonador(tabela_de_processos, prontos, bloqueados, quantum)

# Inicie o escalonador
escalonador.run()
