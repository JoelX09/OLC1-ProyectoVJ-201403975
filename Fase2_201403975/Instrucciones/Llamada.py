from Abstract.NodoAST import NodoAST
from TS.Tipo import TIPO
from TS.Simbolo import Simbolo
from Abstract.Instruccion import Instruccion
from TS.Excepcion import Excepcion
from TS.TablaSimbolos import TablaSimbolos

class Llamada(Instruccion):
    def __init__(self, nombre, parametros, fila, columna):
        self.nombre = nombre
        self.parametros = parametros
        self.fila = fila
        self.columna = columna
    
    def interpretar(self, tree, table):
        result = tree.getFuncion(self.nombre.lower()) ## OBTENER LA FUNCION
        if result == None: # NO SE ENCONTRO LA FUNCION
            return Excepcion("Semantico", "No se encontro la funcion: " + self.nombre, self.fila, self.columna)
        nuevaTabla = TablaSimbolos(tree.getTSglobal())
        # OBTENER PARAMETROS
        if len(result.parametros) == len(self.parametros): #LA CANTIDAD DE PARAMETROS ES LA ADECUADA
            contador=0
            for expresion in self.parametros: # SE OBTIENE EL VALOR DEL PARAMETRO EN LA LLAMADA
                resultExpresion = expresion.interpretar(tree, table)
                if isinstance(resultExpresion, Excepcion): return resultExpresion

                if self.nombre.lower() == "length":
                    if expresion.tipo != TIPO.CADENA and expresion.tipo != TIPO.ARREGLO:
                        return Excepcion("Semantico", "Tipo de parametro de Length no es Cadena o Arreglo.", self.fila, self.columna)
                    else:
                        simbolo = Simbolo(str(result.parametros[contador]['identificador']), result.parametros[contador]['tipo'], self.fila, self.columna, resultExpresion)
                        resultTabla = nuevaTabla.setTabla(simbolo)
                        if isinstance(resultTabla, Excepcion): return resultTabla
                
                elif self.nombre.lower() == "truncate":
                    if expresion.tipo != TIPO.ENTERO and expresion.tipo != TIPO.DECIMAL:
                        return Excepcion("Semantico", "Tipo de parametro de Truncate no es Entero o Decimal.", self.fila, self.columna)
                    else:
                        simbolo = Simbolo(str(result.parametros[contador]['identificador']), result.parametros[contador]['tipo'], self.fila, self.columna, resultExpresion)
                        resultTabla = nuevaTabla.setTabla(simbolo)
                        if isinstance(resultTabla, Excepcion): return resultTabla

                elif self.nombre.lower() == "round":
                    if expresion.tipo != TIPO.DECIMAL:
                        return Excepcion("Semantico", "Tipo de parametro de Round no es Decimal.", self.fila, self.columna)
                    else:
                        simbolo = Simbolo(str(result.parametros[contador]['identificador']), result.parametros[contador]['tipo'], self.fila, self.columna, resultExpresion)
                        resultTabla = nuevaTabla.setTabla(simbolo)
                        if isinstance(resultTabla, Excepcion): return resultTabla

                elif self.nombre.lower() == "typeof":
                    self.tipo = TIPO.CADENA
                    val = "Nulo"

                    if expresion.tipo == TIPO.ENTERO:
                        val = "INT"
                    elif expresion.tipo == TIPO.DECIMAL:
                        val = "DOUBLE"
                    elif expresion.tipo == TIPO.BOOLEANO:
                        val = "BOOLEAN"
                    elif expresion.tipo == TIPO.CADENA:
                        val = "STRING"
                    elif expresion.tipo == TIPO.CHARACTER:
                        val = "CHAR"
                    elif expresion.tipo == TIPO.ARREGLO:
                        val = "ARREGLO->"

                    simbolo = Simbolo(str(result.parametros[contador]['identificador']), result.parametros[contador]['tipo'], self.fila, self.columna, val)
                    resultTabla = nuevaTabla.setTabla(simbolo)
                    if isinstance(resultTabla, Excepcion): return resultTabla

                elif result.parametros[contador]["tipo"] == expresion.tipo:  # VERIFICACION DE TIPO
                    # CREACION DE SIMBOLO E INGRESARLO A LA TABLA DE SIMBOLOS
                    simbolo = Simbolo(str(result.parametros[contador]['identificador']), result.parametros[contador]['tipo'], self.fila, self.columna, resultExpresion)
                    resultTabla = nuevaTabla.setTabla(simbolo)
                    if isinstance(resultTabla, Excepcion): return resultTabla

                else:
                    return Excepcion("Semantico", "Tipo de dato diferente en Parametros de la llamada.", self.fila, self.columna)
                contador += 1

            
        else: 
            return Excepcion("Semantico", "Cantidad de Parametros incorrecta.", self.fila, self.columna)
    
        value = result.interpretar(tree, nuevaTabla)         # INTERPRETAR EL NODO FUNCION
        if isinstance(value, Excepcion): return value
        self.tipo = result.tipo
        
        return value

    def getNodo(self):
        nodo = NodoAST("LLAMADA A FUNCION")
        nodo.agregarHijo(str(self.nombre))
        parametros = NodoAST("PARAMETROS")
        for param in self.parametros:
            parametros.agregarHijoNodo(param.getNodo())
        nodo.agregarHijoNodo(parametros)
        return nodo #Se va para arriba donde se llame