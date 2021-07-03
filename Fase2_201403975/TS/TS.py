class TS:
    def __init__(self, identificador, tipoSimbolo, tipo, entorno, valor, fila, columna):
        self.identificador = identificador
        self.tipoSimbolo = tipoSimbolo
        self.tipo = tipo
        self.entorno = entorno
        self.valor = valor
        self.fila = fila 
        self.columna = columna

    def getIdentificador(self):
        return self.identificador

    def setIdentificador(self, identificador):
        self.identificador = identificador

    def getTipoSimbolo(self):
        return self.tipoSimbolo

    def setTipoSimbolo(self, tipoSimbolo):
        self.tipoSimbolo = tipoSimbolo

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo = tipo

    def getEntorno(self):
        return self.entorno

    def setEntorno(self, entorno):
        self.entorno = entorno

    def getValor(self):
        return self.valor

    def setValor(self, valor):
        self.valor = valor
    
    def getFila(self):
        return self.fila
    
    def getColumna(self):
        return self.columna