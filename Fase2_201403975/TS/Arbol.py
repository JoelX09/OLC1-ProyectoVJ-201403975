class Arbol:
    def __init__(self, instrucciones):
        self.instrucciones = instrucciones #Clase abstracta que puede ser cualquier cosa
        self.funciones = [] #Pull de funciones
        self.excepciones = []
        self.consola = ""
        self.TSglobal = None
        self.ventana = None
        self.textoRead = "Read"
        self.dot = ""
        self.contador = 0
        self.simbolos = {}
        self.entorno = "Global"

    def getSimbolos(self):
        return self.simbolos

    def addSimbolo(self, simbolo):
        self.simbolos[simbolo.identificador.lower()] = simbolo

    def addSimboloF(self, simbolo):
        self.simbolos[str(simbolo.identificador.lower()) + "##Funcion"] = simbolo
    
    def updateSimbolo(self, identificador, tipo, valor):
        self.simbolos[identificador.lower()].setTipo(tipo)
        self.simbolos[identificador.lower()].setValor(valor)

    def updateSimboloF(self, identificador, tipo, valor):
        self.simbolos[str(identificador.lower()) + "##Funcion"].setTipo(tipo)
        self.simbolos[str(identificador.lower()) + "##Funcion"].setValor(valor)

    def getInstrucciones(self):
        return self.instrucciones
    
    def setInstrucciones(self, instrucciones):
        self.instrucciones = instrucciones
    
    def getExcepciones(self):
        return self.excepciones

    def setExcepciones(self, excepciones):
        self.excepciones = excepciones

    def getConsola(self):
        return self.consola

    def setConsola(self, consola):
        self.consola = consola

    def updateConsola(self, cadena): #Hace referencia a la consola que tengo, todos los prints, la salida del interprete
        self.consola += str(cadena) + "\n"

    def getTSglobal(self):
        return self.TSglobal

    def setTSglobal(self, TSglobal):
        self.TSglobal = TSglobal

    def getFunciones(self):
        return self.funciones

    def getFuncion(self, nombre):
        for funcion in self.funciones:
            if funcion.nombre == nombre:
                return funcion
        return None

    def addFuncion(self, funcion):
        self.funciones.append(funcion)

    def getDot(self, raiz): ## DEVUELVE EL STRING DE LA GRAFICA EN GRAPHVIZ
        self.dot = ""
        self.dot += "digraph {\n"
        self.dot += "n0[label=\"" + raiz.getValor().replace("\"", "\\\"") + "\"];\n"
        self.contador = 1
        self.recorrerAST("n0", raiz)
        self.dot += "}"
        return self.dot

    def recorrerAST(self, idPadre, nodoPadre):
        for hijo in nodoPadre.getHijos():
            nombreHijo = "n" + str(self.contador)
            self.dot += nombreHijo + "[label=\"" + hijo.getValor().replace("\"", "\\\"") + "\"];\n"
            self.dot += idPadre + "->" + nombreHijo + ";\n"
            self.contador += 1
            self.recorrerAST(nombreHijo, hijo)