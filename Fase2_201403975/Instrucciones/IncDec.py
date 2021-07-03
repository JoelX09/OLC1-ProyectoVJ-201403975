from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion
from TS.Tipo import TIPO

class Incdec(Instruccion):
    def __init__(self, identificador, incdec, fila, columna):
        self.identificador = identificador
        self.incdec = incdec
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        simbolo = table.getTabla(self.identificador.lower())

        if simbolo == None:
            return Excepcion("Semantico", "Variable " + self.identificador + " no encontrada.", self.fila, self.columna)
        
        if self.incdec != None:
            if simbolo.getTipo() == TIPO.ENTERO or simbolo.getTipo() == TIPO.DECIMAL:
                if self.incdec == 1:
                    simbolo.incValor()
                elif self.incdec == 2:
                    simbolo.decValor()
            else:
                return Excepcion("Semantico", "No se puede incrementar o decrementar la variable " + self.identificador + ", tipo incorrecto.", self.fila, self.columna)

        result = table.actualizarTabla(simbolo)

        if isinstance(result, Excepcion): return result
        val = str(simbolo.getTipo())
        val = val.split(".")
        tree.updateSimbolo(self.identificador, val[1], simbolo.getValor())
        return None

    def getNodo(self):
        if self.incdec != None:
            if self.incdec == 1:
                nodo = NodoAST("INCREMENTO")
                nodo.agregarHijo(str(self.identificador))
            elif self.incdec == 2:
                nodo = NodoAST("DECREMENTO")
                nodo.agregarHijo(str(self.identificador))
        return nodo