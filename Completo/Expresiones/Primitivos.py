from Abstract.Instruccion import Instruccion

class Primitivos(Instruccion): #Indico que heredo de Instruccion, esta clase es un nodo
    def __init__(self, tipo, valor, fila, columna):
        self.tipo = tipo
        self.valor = valor
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        return self.valor

    # def getVal(self): #La puse, es temporal
    #     return self.valor