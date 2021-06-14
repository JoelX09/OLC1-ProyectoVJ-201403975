from Instrucciones.Continue import Continue
from Abstract.Instruccion import Instruccion
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break

class For(Instruccion):
    def __init__(self, decAsig, condicion, actualizacion, instrucciones, fila, columna):
        self.decAsig = decAsig
        self.condicion = condicion
        self.actualizacion = actualizacion
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        nuevaTablaFor = TablaSimbolos(table) #Creo el entorno del for
        decAsig = self.decAsig.interpretar(tree, nuevaTablaFor)
        if isinstance(decAsig, Excepcion): return decAsig

        while True:
            condicion = self.condicion.interpretar(tree, nuevaTablaFor)
            if isinstance(condicion, Excepcion): return condicion

            if self.condicion.tipo == TIPO.BOOLEANO:
                if bool(condicion) == True:   # VERIFICA SI ES VERDADERA LA CONDICION
                    nuevaTabla = TablaSimbolos(nuevaTablaFor)       #NUEVO ENTORNO, entorno de la ejecucion de cada pasada
                    for instruccion in self.instrucciones:
                        result = instruccion.interpretar(tree, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL FOR
                        if isinstance(result, Excepcion) :
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString())
                        if isinstance(result, Break): return None #Return para que se salga definitivamente
                        if isinstance(result, Continue): break #Se salta las instrucciones
                    actualizacion = self.actualizacion.interpretar(tree, nuevaTablaFor) #Actualizacion del ciclo
                    if isinstance(actualizacion, Excepcion): return actualizacion
                else:
                    break
            else:
                return Excepcion("Semantico", "Tipo de dato no booleano en FOR.", self.fila, self.columna)