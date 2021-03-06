from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from Instrucciones.Funcion import Funcion

class TypeOf(Funcion):
    def __init__(self, nombre, parametros, instrucciones, fila, columna):
        self.nombre = nombre.lower()
        self.parametros = parametros
        self.instrucciones = instrucciones # No se utlilizan pero se ponen por que se heredan
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.NULO
    
    def interpretar(self, tree, table):
        simbolo = table.getTabla("typeOf##Param1") #Para evitar duplicidad
        if simbolo == None : return Excepcion("Semantico", "No se encontro el parametro de TypoeOf", self.fila, self.columna)
        
        self.tipo = TIPO.CADENA
        
        return simbolo.getValor()