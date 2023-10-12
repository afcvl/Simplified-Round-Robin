class BCP:
    def __init__(self,process_name, instrucoes, program_counter, register1, register2):
        self.process_name = process_name
        self.instrucoes = instrucoes
        self.program_counter = program_counter 
        self.tempo_de_espera = 0
        self.register1 = register1
        self.register2 = register2
    
    def incrementa_pc(self):
        self.program_counter += 1
        
    def decrementa_espera(self):
        self.tempo_de_espera -= 1