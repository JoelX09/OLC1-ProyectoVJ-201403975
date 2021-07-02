from Abstract.NodoAST import NodoAST
from Abstract.Instruccion import Instruccion
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO, OperadorLogico

class Logica(Instruccion):
    def __init__(self, operador, OperacionIzq, OperacionDer, fila, columna):
        self.operador = operador
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.BOOLEANO

    
    def interpretar(self, tree, table):
        izq = self.OperacionIzq.interpretar(tree, table)
        if isinstance(izq, Excepcion): return izq
        if self.OperacionDer != None:
            der = self.OperacionDer.interpretar(tree, table)
            if isinstance(der, Excepcion): return der

        if self.operador == OperadorLogico.AND:
            if self.OperacionDer.tipo == TIPO.NULO or self.OperacionIzq.tipo == TIPO.NULO: 
                return Excepcion("Semantico", "No se puede operar un && con un valor nulo", self.fila, self.columna)

            if self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) and self.obtenerVal(self.OperacionDer.tipo, der)
            return Excepcion("Semantico", "Tipo Erroneo de operacion para &&.", self.fila, self.columna)
        
        elif self.operador == OperadorLogico.OR:
            if self.OperacionDer.tipo == TIPO.NULO or self.OperacionIzq.tipo == TIPO.NULO: 
                return Excepcion("Semantico", "No se puede operar un || con un valor nulo", self.fila, self.columna)

            if self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) or self.obtenerVal(self.OperacionDer.tipo, der)
            return Excepcion("Semantico", "Tipo Erroneo de operacion para ||.", self.fila, self.columna)
        
        elif self.operador == OperadorLogico.NOT:
            if self.OperacionIzq.tipo == TIPO.NULO: 
                return Excepcion("Semantico", "No se puede negar ! con un valor nulo", self.fila, self.columna)

            if self.OperacionIzq.tipo == TIPO.BOOLEANO:
                return not self.obtenerVal(self.OperacionIzq.tipo, izq)
            return Excepcion("Semantico", "Tipo Erroneo de operacion para !.", self.fila, self.columna)

        return Excepcion("Semantico", "Tipo de operacion no especificada.", self.fila, self.columna)

    def getNodo(self):
        nodo = NodoAST("Logica")
        
        if self.OperacionDer != None: #Si no es operacion Unaria Ej !FALSE
            nodo.agregarHijoNodo(self.OperacionIzq.getNodo())
            nodo.agregarHijo(self.obtenerOperador(self.operador))
            nodo.agregarHijoNodo(self.OperacionDer.getNodo())
        else:
            nodo.agregarHijo(self.obtenerOperador(self.operador))
            nodo.agregarHijoNodo(self.OperacionIzq.getNodo())

        return nodo

    def obtenerOperador(self, op):
        if op == OperadorLogico.NOT:
            return "!"
        elif op == OperadorLogico.AND:
            return "&&"
        elif op == OperadorLogico.OR:
            return "||"

    def obtenerVal(self, tipo, val):
        if tipo == TIPO.ENTERO:
            return int(val)
        elif tipo == TIPO.DECIMAL:
            return float(val)
        elif tipo == TIPO.BOOLEANO:
            return bool(val)
        return str(val)