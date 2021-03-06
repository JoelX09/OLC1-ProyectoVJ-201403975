from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from Instrucciones.Funcion import Funcion
from Expresiones.Primitivos import Primitivos

class ToLower(Funcion):
    def __init__(self, nombre, parametros, instrucciones, fila, columna):
        self.nombre = nombre.lower()
        self.parametros = parametros
        self.instrucciones = instrucciones # No se utlilizan pero se ponen por que se heredan
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.NULO
    
    def interpretar(self, tree, table):
        simbolo = table.getTabla("toLower##Param1") #Para evitar duplicidad
        if simbolo == None : return Excepcion("Semantico", "No se encontro el parametro de ToLower", self.fila, self.columna)

        if simbolo.getTipo() != TIPO.CADENA:
            return Excepcion("Semantico", "Tipo de parametro de ToLower no es cadena.", self.fila, self.columna)

        val = simbolo.getValor()

        if isinstance(val, Primitivos):
            val = val.interpretar(tree, table)

        self.tipo = simbolo.getTipo()
        return val.lower()