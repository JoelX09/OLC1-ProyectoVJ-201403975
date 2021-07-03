from Abstract.NodoAST import NodoAST
from Instrucciones.Return import Return
from Abstract.Instruccion import Instruccion
from TS.Excepcion import Excepcion
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break

class Switch(Instruccion):
    def __init__(self, expresion, cases, default, fila, columna):
        self.expresion = expresion
        self.cases = cases
        self.default = default
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        anterior = tree.entorno
        tree.entorno = "Switch"
        expresion = self.expresion.interpretar(tree, table) #Interpreto de de que tipo es la expresion, error | primitivo | logico | etc
        if isinstance(expresion, Excepcion): 
            tree.entorno = anterior
            return expresion #Siempre (?) despues de interpretar una condicion

        #nuevaTablaSwitch = TablaSimbolos(table)       #NUEVO ENTORNO que es este switch, Preguntar
        cumple = False

        if self.cases != None:
            
            for case in self.cases:
                expresionCase = case.expresion.interpretar(tree, table) #EJECUTA INSTRUCCION ADENTRO DEL CASE

                if isinstance(expresionCase, Excepcion): #Si hubo en un error en la expresion del case
                    tree.getExcepciones().append(expresionCase)
                    tree.updateConsola(expresionCase.toString())
                    continue

                if self.expresion.tipo == case.expresion.tipo:
                    if expresion == expresionCase:
                        nuevaTabla = TablaSimbolos(table)
                        for instruccion in case.instrucciones:
                            result = instruccion.interpretar(tree, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL CASE
                            if isinstance(result, Excepcion) : #Reporte el CASE y nos recuperamos dentro del Case
                                tree.getExcepciones().append(result)
                                tree.updateConsola(result.toString())
                            if isinstance(result, Break): 
                                cumple = True
                                tree.entorno = anterior
                                return None
                            if isinstance(result, Return): 
                                cumple = True
                                tree.entorno = anterior
                                return result
        
        if not cumple:
            if self.default != None:
                nuevaTabla = TablaSimbolos(table)       #NUEVO ENTORNO que es el default
                for instruccion in self.default.instrucciones:
                    result = instruccion.interpretar(tree, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL IF
                    if isinstance(result, Excepcion) : #Reporte el if y nos recuperamos dentro del if
                        tree.getExcepciones().append(result)
                        tree.updateConsola(result.toString())
                    if isinstance(result, Break): 
                        tree.entorno = anterior
                        return None #Return para que se salga definitivamente
                    if isinstance(result, Return): 
                        tree.entorno = anterior 
                        return result

        tree.entorno = anterior
        return None

    def getNodo(self):
        nodo = NodoAST("SWITCH")

        if self.cases != None:
            #cases = NodoAST("CASES")
            for instr in self.cases:
                nodo.agregarHijoNodo(instr.getNodo())
            #nodo.agregarHijoNodo(cases)
        
        if self.default != None:
            #default = NodoAST("DEFAULT")
            nodo.agregarHijoNodo(self.default.getNodo())
            #nodo.agregarHijoNodo(default)

        return nodo