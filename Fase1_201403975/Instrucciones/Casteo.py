from TS.Tipo import TIPO
from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion
from TS.Simbolo import Simbolo

class Casteo(Instruccion):
    def __init__(self, tipo, expresion, fila, columna):
        self.tipo = tipo
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        value = self.expresion.interpretar(tree, table) # Valor a asignar a la variable
        if isinstance(value, Excepcion): return value

        tipo = None

        if self.expresion.tipo == TIPO.BOOLEANO:
            tipo = "Boolean"
        elif self.expresion.tipo == TIPO.CHARACTER:
            tipo = "Char"
        elif self.expresion.tipo == TIPO.CADENA:
            tipo = "String"
        elif self.expresion.tipo == TIPO.DECIMAL:
            tipo = "Double"
        elif self.expresion.tipo == TIPO.ENTERO:
            tipo = "Int"

        if self.tipo == TIPO.DECIMAL:
            if self.expresion.tipo == TIPO.ENTERO:
                return float(value)
            elif self.expresion.tipo == TIPO.CHARACTER:
                if len(value) > 1:
                    return Excepcion("Semantico", "Char incorrecto. El largo es mayor.", self.fila, self.columna)
                else:
                    return float(ord(value))
            else:
                return Excepcion("Semantico", "Tipo " + tipo + " no se puede castear a Double.", self.fila, self.columna)
        
        elif self.tipo == TIPO.ENTERO:
            if self.expresion.tipo == TIPO.DECIMAL:
                return int(value)
            elif self.expresion.tipo == TIPO.CHARACTER:
                if len(value) > 1:
                    return Excepcion("Semantico", "Char incorrecto. El largo es mayor.", self.fila, self.columna)
                else:
                    return ord(value)
            else:
                return Excepcion("Semantico", "Tipo " + tipo + " no se puede castear a Int.", self.fila, self.columna)

        elif self.tipo == TIPO.CADENA:
            if self.expresion.tipo == TIPO.ENTERO or tipo == TIPO.DECIMAL:
                return str(value)
            else:
                return Excepcion("Semantico", "Tipo " + tipo + " no se puede castear a String.", self.fila, self.columna)

        elif self.tipo == TIPO.CHARACTER:
            if self.expresion.tipo == TIPO.ENTERO:
                return chr(value)
            else:
                return Excepcion("Semantico", "Tipo " + tipo + " no se puede castear a Char.", self.fila, self.columna)