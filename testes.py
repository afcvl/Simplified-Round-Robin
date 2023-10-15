class BCP:
    def __init__(self,process_name):
        self.process_name = process_name
        self.program_counter = 0

    def incrementa_pc(self):
        self.program_counter += 1
        
    def decrementa_espera(self):
        self.tempo_de_espera -= 1
        
    def is_equal(self, processo2):
        
        return self.process_name == processo2.process_name


obj1 = BCP('nnn')

obj2 = BCP('nnn')

obj = BCP('nnn')


print(obj.is_equal(obj2))