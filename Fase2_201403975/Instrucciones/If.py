from Abstract.NodoAST import NodoAST
from Instrucciones.Return import Return
from Instrucciones.Continue import Continue
from Instrucciones.Break import Break
from Abstract.Instruccion import Instruccion
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from TS.TablaSimbolos import TablaSimbolos

class If(Instruccion):
    def __init__(self, condicion, instruccionesIf, instruccionesElse, ElseIf, fila, columna):
        self.condicion = condicion
        self.instruccionesIf = instruccionesIf
        self.instruccionesElse = instruccionesElse
        self.elseIf = ElseIf
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        anterior = tree.entorno
        tree.entorno = "If"
        condicion = self.condicion.interpretar(tree, table) #Interpreto de de que tipo es condicion, error | primitivo | logico | etc
        if isinstance(condicion, Excepcion): 
            tree.entorno = anterior
            return condicion #Siempre (?) despues de interpretar una condicion

        if self.condicion.tipo == TIPO.BOOLEANO:
            if bool(condicion) == True:   # VERIFICA SI ES VERDADERA LA CONDICION
                nuevaTabla = TablaSimbolos(table)       #NUEVO ENTORNO que es este if
                for instruccion in self.instruccionesIf:
                    result = instruccion.interpretar(tree, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL IF
                    if isinstance(result, Excepcion) : #Reporte el if y nos recuperamos dentro del if
                        tree.getExcepciones().append(result)
                        tree.updateConsola(result.toString())
                    if isinstance(result, Break): 
                        tree.entorno = anterior
                        return result #Return para que se salga definitivamente
                    if isinstance(result, Continue): 
                        tree.entorno = anterior
                        return result #Return para que se salga definitivamente
                    if isinstance(result, Return): 
                        tree.entorno = anterior
                        return result
            else:               #ELSE
                if self.instruccionesElse != None:
                    nuevaTabla = TablaSimbolos(table)       #NUEVO ENTORNO
                    for instruccion in self.instruccionesElse:
                        result = instruccion.interpretar(tree, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL IF
                        if isinstance(result, Excepcion) :
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString())
                        if isinstance(result, Break): 
                            tree.entorno = anterior
                            return result #Return para que se salga definitivament
                        if isinstance(result, Continue): 
                            tree.entorno = anterior
                            return result #Return para que se salga definitivamente
                        if isinstance(result, Return): 
                            tree.entorno = anterior
                            return result
                elif self.elseIf != None:
                    result = self.elseIf.interpretar(tree, table)
                    if isinstance(result, Excepcion): 
                        tree.entorno = anterior
                        return result
                    if isinstance(result, Break): 
                        tree.entorno = anterior
                        return result #Return para que se salga definitivament
                    if isinstance(result, Continue): 
                        tree.entorno = anterior
                        return result #Return para que se salga definitivamente
                    if isinstance(result, Return): 
                        tree.entorno = anterior
                        return result

        else:
            tree.entorno = anterior
            return Excepcion("Semantico", "Tipo de dato no booleano en IF.", self.fila, self.columna)
        tree.entorno = anterior

    def getNodo(self):
        nodo = NodoAST("IF")

        instruccionesIf = NodoAST("INSTRUCCIONES IF")
        for instr in self.instruccionesIf:
            instruccionesIf.agregarHijoNodo(instr.getNodo())
        nodo.agregarHijoNodo(instruccionesIf)

        if self.instruccionesElse != None:
            instruccionesElse = NodoAST("INSTRUCCIONES ELSE")
            for instr in self.instruccionesElse:
                instruccionesElse.agregarHijoNodo(instr.getNodo())
            nodo.agregarHijoNodo(instruccionesElse) 
            
        elif self.elseIf != None:
            nodo.agregarHijoNodo(self.elseIf.getNodo())

        return nodo