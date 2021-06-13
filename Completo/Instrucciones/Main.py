from Instrucciones.Continue import Continue
from Instrucciones.Break import Break
from Abstract.Instruccion import Instruccion
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from TS.TablaSimbolos import TablaSimbolos

class Main(Instruccion):
    def __init__(self, instrucciones, fila, columna):
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        nuevaTabla = TablaSimbolos(table)       #NUEVO ENTORNO que es este Main
        for instruccion in self.instrucciones:
            result = instruccion.interpretar(tree, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL Main
            if isinstance(result, Excepcion) : #Reporte el Main y nos recuperamos dentro del Main
                tree.getExcepciones().append(result)
                tree.updateConsola(result.toString())
            if isinstance(result, Break): 
                err = Excepcion("Semantico", "BREAK invalido en Main", instruccion.fila, instruccion.columna)
                tree.getExcepciones().append(err)
                tree.updateConsola(err.toString())
            if isinstance(result, Continue): 
                err = Excepcion("Semantico", "CONTINUE invalido en Main", instruccion.fila, instruccion.columna)
                tree.getExcepciones().append(err)
                tree.updateConsola(err.toString())