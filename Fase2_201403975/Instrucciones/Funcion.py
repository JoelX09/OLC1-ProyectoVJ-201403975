from TS.TS import TS
from Abstract.NodoAST import NodoAST
from TS.Tipo import TIPO
from Instrucciones.Return import Return
from Abstract.Instruccion import Instruccion
from TS.Excepcion import Excepcion
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break

class Funcion(Instruccion):
    def __init__(self, nombre, parametros, instrucciones, fila, columna):
        self.nombre = nombre.lower()
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.NULO
    
    def interpretar(self, tree, table):
        nuevaTabla = TablaSimbolos(table)
        anterior = tree.entorno
        tree.entorno = "Funcion " + str(self.nombre)

        tree.addSimboloF(TS(str(self.nombre), "Funcion", "--", "--", "--", self.fila, self.columna))

        for instruccion in self.instrucciones:      # REALIZAR LAS ACCIONES
            value = instruccion.interpretar(tree,nuevaTabla)
            if isinstance(value, Excepcion) :
                tree.getExcepciones().append(value)
                tree.updateConsola(value.toString())
            if isinstance(value, Break): 
                err = Excepcion("Semantico", "Sentencia BREAK fuera de ciclo", instruccion.fila, instruccion.columna)
                tree.getExcepciones().append(err)
                tree.updateConsola(err.toString())
            if isinstance(value, Return):
                self.tipo = value.tipo
                val = str(self.tipo)
                val = val.split(".")
                tree.updateSimboloF(self.nombre, val[1], "--")
                tree.entorno = anterior
                return value.result
        tree.entorno = anterior
        return None

    def getNodo(self):
        nodo = NodoAST("FUNCION")
        nodo.agregarHijo(str(self.nombre))
        parametros = NodoAST("PARAMETROS")
        for param in self.parametros:
            parametro = NodoAST("PARAMETRO")
            parametro.agregarHijo(self.valorTipo(param["tipo"]))
            parametro.agregarHijo(param["identificador"])
            parametros.agregarHijoNodo(parametro)
        nodo.agregarHijoNodo(parametros)
        
        instrucciones = NodoAST("INSTRUCCIONES")
        for instru in self.instrucciones:
            instrucciones.agregarHijoNodo(instru.getNodo())
        nodo.agregarHijoNodo(instrucciones)
        return nodo #Se va para arriba donde se llame

    def valorTipo(self, valor):
        if valor == TIPO.ENTERO:
            return "INT"
        elif valor == TIPO.DECIMAL:
            return "DOUBLE"
        elif valor == TIPO.BOOLEANO:
            return "BOOLEAN"
        elif valor == TIPO.CHARACTER:
            return "CHAR"
        elif valor == TIPO.CADENA:
            return "STRING"
        elif valor == TIPO.ARREGLO:
            return "ARREGLO"