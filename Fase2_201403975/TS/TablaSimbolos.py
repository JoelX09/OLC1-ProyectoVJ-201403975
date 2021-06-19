from TS.Excepcion import Excepcion
from TS.Tipo import TIPO

class TablaSimbolos:
    def __init__(self, anterior = None):
        self.tabla = {} #Diccionario vacio, es como una tabla hash
        self.anterior = anterior

    def setTabla(self, simbolo): #Agregar una variable/Simbolo
        if simbolo.id.lower() in self.tabla:
            return Excepcion("Semantico", "Variable " + simbolo.id + " ya existe", simbolo.fila, simbolo.columna)
        else:
            self.tabla[simbolo.id.lower()] = simbolo
            return None #Se agrego correctamente

    def getTabla(self, id): #Obtener una variable/Simbolo
        tablaActual = self
        while tablaActual != None:
            if id.lower() in tablaActual.tabla:
                return tablaActual.tabla[id.lower()] #Retorna simbolo
            else:
                tablaActual = tablaActual.anterior
        return None #No existe el simbolo

    def actualizarTabla(self, simbolo):
        tablaActual = self
        while tablaActual != None:
            idMinuscula = simbolo.id.lower()
            if idMinuscula in tablaActual.tabla :
                if tablaActual.tabla[idMinuscula].getTipo() == TIPO.NULO:
                    tablaActual.tabla[idMinuscula].setValor(simbolo.getValor())
                    tablaActual.tabla[idMinuscula].setTipo(simbolo.getTipo())
                    return None             #VARIABLE ACTUALIZADA
                elif tablaActual.tabla[idMinuscula].getTipo() == simbolo.getTipo() or simbolo.getTipo() == TIPO.NULO: #Revisar si aqui lo agrego
                    tablaActual.tabla[idMinuscula].setValor(simbolo.getValor())
                    tablaActual.tabla[idMinuscula].setTipo(simbolo.getTipo())
                    return None             #VARIABLE ACTUALIZADA
                return Excepcion("Semantico", "Tipo de dato Diferente en Asignacion", simbolo.getFila(), simbolo.getColumna())
            else:
                tablaActual = tablaActual.anterior
        return Excepcion("Semantico", "Variable No encontrada en Asignacion", simbolo.getFila(), simbolo.getColumna())