from Expresiones.Primitivos import Primitivos
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from Instrucciones.Funcion import Funcion

class Length(Funcion):
    def __init__(self, nombre, parametros, instrucciones, fila, columna):
        self.nombre = nombre.lower()
        self.parametros = parametros
        self.instrucciones = instrucciones # No se utlilizan pero se ponen por que se heredan
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.NULO
    
    def interpretar(self, tree, table):
        simbolo = table.getTabla("length##Param1") #Para evitar duplicidad
        if simbolo == None : return Excepcion("Semantico", "No se encontro el parametro de Length", self.fila, self.columna)

        self.tipo = TIPO.ENTERO

        val = simbolo.getValor()

        if isinstance(val, Primitivos):
            val = val.interpretar(tree, table)

        return len(val)