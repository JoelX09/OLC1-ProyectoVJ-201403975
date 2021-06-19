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

        if self.expresion.tipo == TIPO.NULO:
            return Excepcion("Semantico", "Valor nulo no se puede castear.", self.fila, self.columna)

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
            elif self.expresion.tipo == TIPO.CADENA:
                    try:
                        float(value)
                        return float(value)
                    except ValueError:
                        return Excepcion("Semantico", "La cadena " + value + " no se puede castear a Double.", self.fila, self.columna)

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
            elif self.expresion.tipo == TIPO.CADENA:
                if value.isdigit():
                    return int(value)
                else:
                    return Excepcion("Semantico", "La cadena " + value + " no se puede castear a Int.", self.fila, self.columna)
            else:
                return Excepcion("Semantico", "Tipo " + tipo + " no se puede castear a Int.", self.fila, self.columna)

        elif self.tipo == TIPO.CADENA:
            if self.expresion.tipo == TIPO.ENTERO or self.expresion.tipo == TIPO.DECIMAL:
                return str(value)
            else:
                return Excepcion("Semantico", "Tipo " + tipo + " no se puede castear a String.", self.fila, self.columna)

        elif self.tipo == TIPO.CHARACTER:
            if self.expresion.tipo == TIPO.ENTERO:
                return chr(value)
            else:
                return Excepcion("Semantico", "Tipo " + tipo + " no se puede castear a Char.", self.fila, self.columna)

        elif self.tipo == TIPO.BOOLEANO:
            if self.expresion.tipo == TIPO.CADENA:
                if value.lower() == 'true':
                    return True
                elif value.lower() == 'false':
                    return False
                else: 
                    return Excepcion("Semantico", "La cadena " + value + " no se puede castear a Boolean.", self.fila, self.columna)
            else:
                return Excepcion("Semantico", "Tipo " + tipo + " no se puede castear a Boolean.", self.fila, self.columna)