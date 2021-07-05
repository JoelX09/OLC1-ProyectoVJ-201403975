from TS.Tipo import TIPO
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion
from TS.Simbolo import Simbolo
import copy

class DeclaracionT3(Instruccion):
    def __init__(self, tipo, dimensiones, identificador, identificador2, fila, columna):
        self.tipo = tipo
        self.dimensiones = dimensiones
        self.identificador = identificador
        self.identificador2 = identificador2
        self.fila = fila
        self.columna = columna
        self.arreglo = True

    def interpretar(self, tree, table):

        simbolo = table.getTabla(self.identificador2.lower())
        
        if simbolo == None:
            return Excepcion("Semantico", "Variable " + self.identificador2 + " no encontrada.", self.fila, self.columna)
        
        if not simbolo.getArreglo(): 
            return Excepcion("Semantico", "Variable " + self.identificador2 + " no es un arreglo.", self.fila, self.columna)

        if self.tipo != simbolo.getTipo(): 
            return Excepcion("Semantico", "Tipo de dato diferente en Asignacion de Arreglo.", self.fila, self.columna)

        simbolo.setId(self.identificador)
        result = table.setTabla(simbolo)
        if isinstance(result, Excepcion): return result
        return None

    def getNodo(self):
        nodo = NodoAST("DECLARACION ARREGLO")
        val = str(self.tipo)
        val = val.split(".")
        nodo.agregarHijo(val[1])
        nodo.agregarHijo(str(self.dimensiones))
        nodo.agregarHijo(str(self.identificador))
        # exp = NodoAST("EXPRESIONES DE LAS DIMENSIONES")
        # for expresion in self.expresiones:
        #     exp.agregarHijoNodo(expresion.getNodo())
        # nodo.agregarHijoNodo(exp)
        return nodo