from Abstract.NodoAST import NodoAST
from TS.Tipo import TIPO
from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion

class Identificador(Instruccion):
    def __init__(self, identificador, incdec, fila, columna):
        self.identificador = identificador
        self.fila = fila
        self.columna = columna
        self.tipo = None
        self.incdec = incdec

    def interpretar(self, tree, table):
        simbolo = table.getTabla(self.identificador.lower())

        if simbolo == None:
            return Excepcion("Semantico", "Variable " + self.identificador + " no encontrada.", self.fila, self.columna)

        self.tipo = simbolo.getTipo()

        if self.incdec != None:
            if self.tipo == TIPO.ENTERO or self.tipo == TIPO.DECIMAL:
                if self.incdec == 1:
                    return simbolo.getValor() + 1
                elif self.incdec == 2:
                    return simbolo.getValor() -1
            else:
                return Excepcion("Semantico", "No se puede incrementar o decrementar la variable " + self.identificador + ", tipo incorrecto.", self.fila, self.columna)
        
        return simbolo.getValor()

    def getNodo(self):
        nodo = NodoAST("Identificador")
        nodo.agregarHijo(str(self.identificador))
        if self.incdec != None:
            if self.incdec == 1:
                nodo.agregarHijo("INCREMENTO")
            elif self.incdec == 2:
                nodo.agregarHijo("DECREMENTO")
        return nodo #Se va para arriba donde se llame