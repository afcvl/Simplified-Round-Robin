from BCP import BCP
        
        
prontos = []

block = []

tabela_de_processos = []



class Escalonador:
    def __init__(self, tabela_de_processos, pronto, bloqueado):
        self.tabela_de_processos = tabela_de_processos
        self.lista_pronto = pronto
        self.lista_bloqueado = bloqueado
        self.quantum = 3
        
    def decrementa_espera_bloqueados(self):
        i = 0
        processos_liberados = []
        while i < len(self.lista_bloqueado):  # decremento do tempo dos bloqueados
            
            processo_bloqueado = self.lista_bloqueado[i]
            processo_bloqueado.decrementa_espera()
            
            if processo_bloqueado.tempo_de_espera == 0:
                processos_liberados.append(i)
                
            i += 1
            
        for i in list(reversed(processos_liberados)):  # liberacão dos processos prontos
            self.lista_bloqueado.pop(i)
            self.lista_pronto.insert(len(self.lista_pronto), processo_bloqueado)
            
            
    
    def run(self):
        while True:
            
            processo_atual = self.lista_pronto.pop(0)
            
            
            # ------------ Quantum ------------
            step = 0
            n_comp = 0
            while step < self.quantum:
                
                instrucao = processo_atual.instrucoes[processo_atual.program_counter]
                
                processo_atual.incrementa_pc()
                
                if instrucao == 'E/S':
                    processo_atual.tempo_de_espera = 5     # hard code para o tempo minimo de espera apos ser bloqueado
                    
                    self.lista_bloqueado.insert(len(self.lista_bloqueado), processo_atual)  # insere o processo no fim da fila de block
                    
                    break
                
                elif instrucao == 'COM':
                    n_comp += 1
                    pass
                
                elif instrucao == 'SAIDA':
                    
                    for proc in self.tabela_de_processos:      # remoção do processo da tabela de processos   
                                                                                                #####     QUEBRADOOO ############
                        if tabela_de_processos.is_equal(processo_atual):
                            tabela_de_processos.pop(proc)
                        
                        
                    break
                    
                else:
                    registrador = instrucao[0]   # registrador alvo
                    
                    valor = registrador.split('=')   # valor 
                    valor = valor[-1]
                    
                    if registrador == 'X':
                        processo_atual.register1 = valor
                    else:
                        processo_atual.register2 = valor
                    
                    n_comp += 1
                    
                
                step += 1
                
            if n_comp == 3:                     # insere novamente o processo na lista de prontos
                prontos.insert(len(prontos), processo_atual)

            self.decrementa_espera_bloqueados()
            
            
            


## =========================== Carrega arquivos ===========================================
def carrega_arquivos():
    for i in range(11):
        if i == 0:
            continue
        
        path = 'programas/' + '0' + f'{i}.txt'
        if i == 10:
            path = 'programas/' + f'{i}.txt'
                     
        
        with open(path, 'r') as file:
            codigo_fonte = file.read()
            instrucoes = codigo_fonte.split('\n')
            
        processo = BCP(instrucoes[0], instrucoes[1:-1] , 0, None, None)
                
        tabela_de_processos.append(processo)
        prontos.append(processo)
        
    return tabela_de_processos, prontos
    ## ==================================================================================


tabela_de_processos, prontos = carrega_arquivos()

escalonador = Escalonador(tabela_de_processos, prontos, [])

escalonador.run()

# processo = BCP(1)

# processo.incrementa_pc()

# print(processo.program_counter)