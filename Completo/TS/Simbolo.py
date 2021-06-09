class Simbolo:
    def __init__(self, identificador, tipo, fila, columna, valor): #Constructor
        self.id = identificador
        self.tipo = tipo
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
    
    def getFila(self):
        return self.fila
    
    def getColumna(self):
        return self.columna