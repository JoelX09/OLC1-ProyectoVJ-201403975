from abc import ABC, abstractmethod

class Instruccion(ABC): #Nos va a servir para poder heredar
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        super().__init__()

    @abstractmethod
    def interpretar(self, tree, table): #Arbol y tabla de simbolos
        pass

    @abstractmethod
    def getNodo(self):
        pass