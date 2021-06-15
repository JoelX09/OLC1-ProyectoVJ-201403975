from Abstract.Instruccion import Instruccion

class Case(Instruccion):
    def __init__(self, expresion, instrucciones, fila, columna):
        self.expresion = expresion
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        return self