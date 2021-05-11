class Evento(object):

    inicio: float
    fim: float
    tipo: str
    probabilidade: float

    def __init__(self, inicio=0, fim=0, tipo="null", probabilidade=0):
        self.inicio = inicio
        self.fim = fim
        self.tipo = tipo
        self.probabilidade = probabilidade
    
    # def __repr__(self):  
    #     return (self.inicio, self.fim, self.tipo, self.probabilidade)
 