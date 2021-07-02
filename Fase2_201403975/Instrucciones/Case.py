from Abstract.NodoAST import NodoAST
from Abstract.Instruccion import Instruccion

class Case(Instruccion):
    def __init__(self, expresion, instrucciones, fila, columna):
        self.expresion = expresion
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        return self

    def getNodo(self):
        nodo = NodoAST("CASE")
        # expresion = NodoAST("EXPRESION")
        # expresion.agregarHijoNodo(self.expresion.getNodo())
        # nodo.agregarHijoNodo(expresion)

        instrucciones = NodoAST("INSTRUCCIONES CASE")
        for instru in self.instrucciones:
            instrucciones.agregarHijoNodo(instru.getNodo())
        nodo.agregarHijoNodo(instrucciones)
        
        return nodo #Se va para arriba donde se llame