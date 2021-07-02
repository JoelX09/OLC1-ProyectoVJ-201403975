from TS.Tipo import TIPO
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion
from TS.Simbolo import Simbolo

class Declaracion(Instruccion):
    def __init__(self, identificador, fila, columna, expresion=None):
        self.identificador = identificador
        self.tipo = None
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        value = self.expresion.interpretar(tree, table) # Valor a asignar a la variable
        if isinstance(value, Excepcion): return value

        self.tipo = self.expresion.tipo #08/06 - 29:00

        simbolo = Simbolo(str(self.identificador), self.tipo, self.fila, self.columna, value)

        result = table.setTabla(simbolo)

        if isinstance(result, Excepcion): return result
        return None

    def getNodo(self):
        nodo = NodoAST("DECLARACION")
        nodo.agregarHijo(str(self.identificador))
        # if self.expresion != None:
        #     if self.expresion.tipo != TIPO.NULO:
        nodo.agregarHijoNodo(self.expresion.getNodo())
        return nodo #Se va para arriba donde se llame