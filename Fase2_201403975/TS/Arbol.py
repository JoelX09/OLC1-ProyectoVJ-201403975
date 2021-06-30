class Arbol:
    def __init__(self, instrucciones):
        self.instrucciones = instrucciones #Clase abstracta que puede ser cualquier cosa
        self.funciones = [] #Pull de funciones
        self.excepciones = []
        self.consola = ""
        self.TSglobal = None
        self.ventana = None

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