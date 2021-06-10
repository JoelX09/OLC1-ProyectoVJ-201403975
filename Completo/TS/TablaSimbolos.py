from TS.Excepcion import Excepcion
from TS.Tipo import TIPO

class TablaSimbolos:
    def __init__(self, anterior = None):
        self.tabla = {} #Diccionario vacio, es como una tabla hash
        self.anterior = anterior
        self.funciones = []

    def setTabla(self, simbolo): #Agregar una variable/Simbolo
        if simbolo.id.lower() in self.tabla:
            return Excepcion("Semantico", "Variable " + simbolo.id + " ya existe", simbolo.fila, simbolo.columna)
        else:
            self.tabla[simbolo.id.lower()] = simbolo
            return None #Se agrego correctamente

    def getTabla(self, id): #Obtener una variable/Simbolo
        tablaActual = self
        while tablaActual != None:
            if id in self.tabla:
                return self.tabla[id] #Retorna simbolo
            else:
                tablaActual = tablaActual.anterior
        return None #No existe el simbolo

    def actualizarTabla(self, simbolo):
        tablaActual = self
        while tablaActual != None:
            if simbolo.id in self.tabla :
                if self.tabla[simbolo.id].getTipo() == simbolo.getTipo() or simbolo.getTipo() == TIPO.NULO: #Revisar si aqui lo agrego
                    self.tabla[simbolo.id].setValor(simbolo.getValor())
                    self.tabla[simbolo.id].setTipo(simbolo.getTipo())
                    return None             #VARIABLE ACTUALIZADA
                return Excepcion("Semantico", "Tipo de dato Diferente en Asignacion", simbolo.getFila(), simbolo.getColumna())
            else:
                tablaActual = tablaActual.anterior
        return Excepcion("Semantico", "Variable No encontrada en Asignacion", simbolo.getFila(), simbolo.getColumna())