from Abstract.NodoAST import NodoAST
from Instrucciones.Return import Return
from Abstract.Instruccion import Instruccion
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break
from Instrucciones.Continue import Continue

class While(Instruccion):
    def __init__(self, condicion, instrucciones, fila, columna):
        self.condicion = condicion
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        anterior = tree.entorno
        tree.entorno = "While"
        while True:
            condicion = self.condicion.interpretar(tree, table)
            if isinstance(condicion, Excepcion): 
                tree.entorno = anterior
                return condicion

            if self.condicion.tipo == TIPO.BOOLEANO:
                if bool(condicion) == True:   # VERIFICA SI ES VERDADERA LA CONDICION
                    nuevaTabla = TablaSimbolos(table)       #NUEVO ENTORNO
                    for instruccion in self.instrucciones:
                        result = instruccion.interpretar(tree, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL IF
                        if isinstance(result, Excepcion) :
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString())
                        if isinstance(result, Break): 
                            tree.entorno = anterior
                            return None #Return para que se salga definitivamente
                        if isinstance(result, Continue): break #Se salta las instrucciones
                        if isinstance(result, Return): 
                            tree.entorno = anterior
                            return result
                else:
                    break
            else:
                tree.entorno = anterior
                return Excepcion("Semantico", "Tipo de dato no booleano en WHILE.", self.fila, self.columna)

        tree.entorno = anterior
    
    def getNodo(self):
        nodo = NodoAST("WHILE")

        instrucciones = NodoAST("INSTRUCCIONES WHILE")
        for instr in self.instrucciones:
            instrucciones.agregarHijoNodo(instr.getNodo())
        nodo.agregarHijoNodo(instrucciones)

        return nodo