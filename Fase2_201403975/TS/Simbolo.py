class Simbolo:
    def __init__(self, identificador, tipo, arreglo, fila, columna, valor): #Constructor
        self.id = identificador
        self.tipo = tipo
        self.arreglo = arreglo
        self.fila = fila
        self.columna = columna
        self.valor = valor

    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo = tipo

    def getValor(self):
        return self.valor

    def setValor(self, valor):
        self.valor = valor

    def incValor(self):
        self.valor = self.valor + 1

    def decValor(self):
        self.valor = self.valor - 1
    
    def getFila(self):
        return self.fila
    
    def getColumna(self):
        return self.columna

    def getArreglo(self):
        return self.arreglo