from Abstract.NodoAST import NodoAST
from Abstract.Instruccion import Instruccion

class Default(Instruccion):
    def __init__(self, instrucciones, fila, columna):
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        return self

    def getNodo(self):
        nodo = NodoAST("DEFAULT")

        instrucciones = NodoAST("INSTRUCCIONES DEFAULT")
        for instr in self.instrucciones:
            instrucciones.agregarHijoNodo(instr.getNodo())
        nodo.agregarHijoNodo(instrucciones)

        return nodo