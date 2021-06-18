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
        expresion = self.expresion.interpretar(tree, table) #Interpreto de de que tipo es la expresion, error | primitivo | logico | etc
        if isinstance(expresion, Excepcion): return expresion #Siempre (?) despues de interpretar una condicion

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
                                return None
                            if isinstance(result, Return): 
                                cumple = True
                                return result
        
        if not cumple:
            if self.default != None:
                nuevaTabla = TablaSimbolos(table)       #NUEVO ENTORNO que es el default
                for instruccion in self.default.instrucciones:
                    result = instruccion.interpretar(tree, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL IF
                    if isinstance(result, Excepcion) : #Reporte el if y nos recuperamos dentro del if
                        tree.getExcepciones().append(result)
                        tree.updateConsola(result.toString())
                    if isinstance(result, Break): return None #Return para que se salga definitivamente
                    if isinstance(result, Return): return result

        return None