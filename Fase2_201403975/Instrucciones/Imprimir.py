from Abstract.NodoAST import NodoAST
from Abstract.Instruccion import Instruccion
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from tkinter import END

class Imprimir(Instruccion):
    def __init__(self, expresion, fila, columna):
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        value = self.expresion.interpretar(tree, table)  # RETORNA CUALQUIER VALOR

        if isinstance(value, Excepcion) :
            return value

        if self.expresion.tipo == TIPO.ARREGLO:
            return Excepcion("Semantico", "No se puede imprimir un arreglo completo", self.fila, self.columna)

        if self.expresion.tipo == TIPO.NULO:
            return Excepcion("Semantico", "No se puede imprimir un tipo NULO", self.fila, self.columna)
        
        tree.updateConsola(value)
        tree.textoRead = value
        tree.salida.delete(1.0, END)
        tree.salida.insert(1.0, tree.getConsola())
        return None

    def getNodo(self):
        nodo = NodoAST("IMPRIMIR")
        if self.expresion.tipo != TIPO.NULO:
            nodo.agregarHijoNodo(self.expresion.getNodo())
        return nodo #Se va para arriba donde se llame