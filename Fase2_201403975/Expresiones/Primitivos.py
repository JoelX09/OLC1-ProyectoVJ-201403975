from TS.Tipo import TIPO
from Abstract.NodoAST import NodoAST
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

    def getNodo(self):
        nodo = NodoAST("Primitivo")
        if self.tipo != TIPO.NULO:
            nodo.agregarHijo(str(self.valor))
            if self.incdec != None:
                if self.incdec == 1:
                    nodo.agregarHijo("INCREMENTO")
                elif self.incdec == 2:
                    nodo.agregarHijo("DECREMENTO")
        return nodo #Se va para arriba donde se llame