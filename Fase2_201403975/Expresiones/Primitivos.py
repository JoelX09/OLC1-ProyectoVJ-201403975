from Abstract.Instruccion import Instruccion

class Primitivos(Instruccion): #Indico que heredo de Instruccion, esta clase es un nodo
    def __init__(self, tipo, valor, incdec, fila, columna):
        self.tipo = tipo
        self.valor = valor
        self.fila = fila
        self.columna = columna
        self.incdec = incdec

    def interpretar(self, tree, table):
        if self.incdec != None:
            if self.incdec == 1:
                self.valor = self.valor + 1
            elif self.incdec == 2:
                self.valor = self.valor - 1
        return self.valor

    # def getVal(self): #La puse, es temporal
    #     return self.valor