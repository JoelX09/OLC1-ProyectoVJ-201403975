from TS.Tipo import TIPO
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion
from TS.Simbolo import Simbolo
import copy

class DeclaracionT2(Instruccion):
    def __init__(self, tipo, dimensiones, identificador, expresion, fila, columna):
        self.identificador = identificador
        self.tipo = tipo
        self.dimensiones = dimensiones
        self.expresion = expresion
        self.fila = fila
        self.columna = columna
        self.arreglo = True

    def interpretar(self, tree, table):
        tipoExp = None
        if self.dimensiones == 1:
            tipoExp = self.expresion[0].tipo
        elif self.dimensiones == 2:
            tipoExp = self.expresion[0][0].tipo
        if self.dimensiones == 3:
            tipoExp = self.expresion[0][0][0].tipo
        if self.dimensiones == 4:
            tipoExp = self.expresion[0][0][0][0].tipo
        
        if self.tipo != tipoExp: #VERIFICACION DE TIPOS
            return Excepcion("Semantico", "Tipo de dato diferente en Arreglo.", self.fila, self.columna)
        # if self.dimensiones != len(self.expresiones):   #VERIFICACION DE DIMENSIONES
        #     return Excepcion("Semantico", "Dimensiones diferentes en Arreglo.", self.fila, self.columna)
        simbolo = Simbolo(str(self.identificador), self.tipo, self.arreglo, self.fila, self.columna, self.expresion)
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
    
    def crearDimensiones(self, tree, table, expresiones):
        arr = []
        if len(expresiones) == 0:
            return None
        dimension = expresiones.pop(0)
        num = dimension.interpretar(tree, table)
        if isinstance(num, Excepcion): return num
        if dimension.tipo != TIPO.ENTERO:
            return Excepcion("Semantico", "Expresion diferente a ENTERO en Arreglo.", self.fila, self.columna)
        contador = 0
        while contador < num:
            arr.append(self.crearDimensiones(tree, table, copy.copy(expresiones)))
            contador += 1
        return arr