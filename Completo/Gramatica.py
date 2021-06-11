'''
Gramatica Proyecto
Vacaciones Junio 2021
'''

from TS.Excepcion import Excepcion

errores = []

reservadas = {
    'int'       : 'RINT',
    'double'    : 'RDOUBLE',
    'boolean'   : 'RBOOLEAN',
    'char'      : 'RCHAR',
    'string'    : 'RSTRING',
    'var'       : 'RVAR',
    'true'      : 'RTRUE',
    'false'     : 'RFALSE',
    'null'      : 'RNULL',
    'if'        : 'RIF',
    'else'      : 'RELSE',
    'break'     : 'RBREAK',
    'print'     : 'RPRINT'
}

tokens  = [
    'PTCOMA',
    'PARA',
    'PARC',
    'LLAVEA',
    'LLAVEC',
    'INC',
    'MAS',
    'DEC',
    'MENOS',
    'POT',
    'POR',
    'DIV',
    'MOD',
    'MENORIGUAL',
    'MENORQUE',
    'MAYORIGUAL',
    'MAYORQUE',
    'IGUALIGUAL',
    'DIFERENTE',
    'AND',
    'OR',
    'NOT',
    'IGUAL',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'CHARACTER',
    'ID'
] + list(reservadas.values())

# Tokens
t_PTCOMA        = r';'
t_PARA          = r'\('
t_PARC          = r'\)'
t_LLAVEA        = r'{'
t_LLAVEC        = r'}'
t_INC           = r'\+\+'
t_MAS           = r'\+'
t_DEC           = r'--'
t_MENOS         = r'-'
t_POT           = r'\*\*'
t_POR           = r'\*'
t_DIV           = r'/'
t_MOD           = r'%'
t_MENORIGUAL    = r'<='
t_MENORQUE      = r'<'
t_MAYORIGUAL    = r'>='
t_MAYORQUE      = r'>'
t_IGUALIGUAL    = r'=='
t_DIFERENTE     = r'=!'
t_AND           = r'&&'
t_OR            = r'\|\|'
t_NOT           = r'!'
t_IGUAL         = r'='

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
     r'[a-zA-Z][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID') #Verifica si no es una reservada y si no se queda como ID
     return t

def t_CADENA(t):
    r'(\".*?\")'
    t.value = t.value[1:-1] # remuevo las comillas
    return t

def t_CHARACTER(t):
    r'(\'.*?\')'
    t.value = t.value[1:-1] # remuevo las comillas
    return t

# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'\#.*[^\r]' #Lo cambie
    t.lexer.lineno += 1

# Caracteres ignorados
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    errores.append(Excepcion("Lexico","Error léxico." + t.value[0] , t.lexer.lineno, find_column(input, t)))
    t.lexer.skip(1)

# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# Construyendo el analizador léxico
import ply.lex as lex
lexer = lex.lex()


# Definición de la gramática

#Abstract
from Abstract.Instruccion import Instruccion
from Instrucciones.Imprimir import Imprimir
from Expresiones.Primitivos import Primitivos
from TS.Tipo import TIPO, OperadorAritmetico, OperadorLogico, OperadorRelacional
from Expresiones.Aritmetica import Aritmetica
from Expresiones.Relacional import Relacional
from Expresiones.Logica import Logica
from Instrucciones.Declaracion import Declaracion
from Expresiones.Identificador import Identificador
from Instrucciones.Asignacion import Asignacion
from Instrucciones.IncDec import Incdec
from Instrucciones.Casteo import Casteo
from Instrucciones.If import If

# Presedencia
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'UNOT'),
    ('left', 'IGUALIGUAL', 'DIFERENTE', 'MAYORQUE', 'MAYORIGUAL', 'MENORQUE', 'MENORIGUAL'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIV', 'MOD'),
    ('nonassoc', 'POT'),
    ('right', 'UMENOS')
)

def p_init(t) :
    'init : instrucciones'
    t[0] = t[1]


#---------------------------Instrucciones---------------------------#
def p_instrucciones_instrucciones_instruccion(t) :
    'instrucciones : instrucciones instruccion'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]

def p_instrucciones_instruccion(t) :
    'instrucciones : instruccion'
    if t[1] == "":
        t[0] = []
    else:    
        t[0] = [t[1]]


#----------------------------Instruccion----------------------------#
def p_fin_instruccion(t):
    '''
    ptc : PTCOMA
        |
    '''
def p_instruccion_variables(t) :
    'instruccion : variables ptc'
    t[0] = t[1]

def p_instruccion_imprimir(t) :
    'instruccion : imprimir ptc'
    t[0] = t[1]

def p_instruccion_if(t):
    'instruccion : if'
    t[0] = t[1]

def p_instruccion_error(t):
    'instruccion : error '
    errores.append(Excepcion("Sintáctico","Error Sintáctico." + str(t[1].value) , t.lineno(1), find_column(input, t.slice[1])))
    t[0] = ""


#-----------------------------Inc y Dec-----------------------------#
def p_inc(t):
    'incdec : INC'
    t[0] = 1
    #print('Se reconocio un inc')

def p_dec(t):
    'incdec :  DEC'
    t[0] = 2
    #print('Se reconocio un dec')

def p_no_incdec(t):
    'incdec : '
    t[0] = None


#-----------------------------Variables-----------------------------#
def p_variables_soloDec(t):
    'variables : RVAR ID'
    #print('Se declaro la variable ' + str(t[2]))
    varnula = Primitivos(TIPO.NULO, 'null', None, t.lineno(1), find_column(input, t.slice[1]))
    t[0] = t[0] = Declaracion(t[2], t.lineno(2), find_column(input, t.slice[2]), varnula) #Revisar <-------------

def p_variables_decAsig(t):
    'variables : RVAR ID IGUAL expresion' 
    #print('Se declaro la var ' + str(t[2])) #Debugger 08/06 - 38:00
    t[0] = Declaracion(t[2], t.lineno(2), find_column(input, t.slice[2]),t[4])
    
def p_variables_decCasteo(t):
    'variables : RVAR ID IGUAL casteo'
    #print('Se declaro la variable ' + str(t[2]) + ' con el valor casteado ' + str(t[4]))
    t[0] = Declaracion(t[2], t.lineno(2), find_column(input, t.slice[2]),t[4])

def p_variables_asig(t):
    'variables : ID IGUAL expresion'
    #print('A la variable ' + str(t[1]) + ' se le asigno el valor ')# + str(t[3].getVal()))
    t[0] = Asignacion(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_variables_asigCasteo(t):
    'variables : ID IGUAL casteo'
    #print('A la variable ' + str(t[1]) + ' se le asigno el valor casteado ' + str(t[3]))
    t[0] = Asignacion(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_variables_asigNulo(t):
    'variables : ID IGUAL RNULL'
    #print('A la variable ' + str(t[1]) + ' se le asigno el valor null')
    varnula = Primitivos(TIPO.NULO, t[3].lower(), None, t.lineno(1), find_column(input, t.slice[1]))
    t[0] = Asignacion(t[1], varnula, t.lineno(1), find_column(input, t.slice[1])) #Revisar <-------------

def p_incdec_variable(t):
    'variables : ID incdec'
    #print("Inc o dec la variable: " + str(t[1]))
    t[0] = Incdec(t[1], t[2], t.lineno(1), find_column(input, t.slice[1]))


#------------------------------Casteo-------------------------------#
def p_casteo(t):
    'casteo : PARA tipo PARC expresion'
    #print('Se casteo a ' + str(t[2]) + ' la expresion ' + str(t[4]))
    t[0] = Casteo(t[2], t[4], t.lineno(1), find_column(input, t.slice[1]))

def p_tipo(t):
    '''tipo : RINT
            | RDOUBLE
            | RCHAR
            | RSTRING
    '''
    if t[1].lower() == 'int':
        t[0] = TIPO.ENTERO
    elif t[1].lower() == 'double':
        t[0] = TIPO.DECIMAL
    elif t[1].lower() == 'char':
        t[0] = TIPO.CHARACTER
    elif t[1].lower() == 'string':
        t[0] = TIPO.CADENA


#----------------------------Expresiones----------------------------#
def p_expresion_binaria(t):
    '''
    expresion : expresion MAS expresion
            | expresion MENOS expresion
            | expresion POR expresion
            | expresion DIV expresion
            | expresion POT expresion
            | expresion MOD expresion
            | expresion MENORQUE expresion
            | expresion MAYORQUE expresion
            | expresion MENORIGUAL expresion
            | expresion MAYORIGUAL expresion
            | expresion IGUALIGUAL expresion
            | expresion DIFERENTE expresion
            | expresion AND expresion
            | expresion OR expresion
    '''
    if t[2] == '+':
        t[0] = Aritmetica(OperadorAritmetico.MAS, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '-':
        t[0] = Aritmetica(OperadorAritmetico.MENOS, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '*':
        t[0] = Aritmetica(OperadorAritmetico.POR, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '/':
        t[0] = Aritmetica(OperadorAritmetico.DIV, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '**':
        t[0] = Aritmetica(OperadorAritmetico.POT, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '%':
        t[0] = Aritmetica(OperadorAritmetico.MOD, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<':
        t[0] = Relacional(OperadorRelacional.MENORQUE, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>':
        t[0] = Relacional(OperadorRelacional.MAYORQUE, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<=':
        t[0] = Relacional(OperadorRelacional.MENORIGUAL, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>=':
        t[0] = Relacional(OperadorRelacional.MAYORIGUAL, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '==':
        t[0] = Relacional(OperadorRelacional.IGUALIGUAL, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '=!':
        t[0] = Relacional(OperadorRelacional.DIFERENTE, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '&&':
        t[0] = Logica(OperadorLogico.AND, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '||':
        t[0] = Logica(OperadorLogico.OR, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))

def p_expresion_unaria(t):
    '''
    expresion : MENOS expresion %prec UMENOS
            | NOT expresion %prec UNOT
    '''
    if t[1] == '-':
        t[0] = Aritmetica(OperadorAritmetico.UMENOS, t[2],None, t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == '!':
        t[0] = Logica(OperadorLogico.NOT, t[2],None, t.lineno(1), find_column(input, t.slice[1]))
        pass

def p_expresion_agrupacion(t):
    '''
    expresion : PARA expresion PARC
    '''
    t[0] = t[2]

def p_expresion_id(t):
    '''expresion : ID incdec'''
    t[0] = Identificador(t[1], t[2], t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_entero(t):
    '''expresion : ENTERO incdec'''
    t[0] = Primitivos(TIPO.ENTERO,t[1], t[2], t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_decimal(t):
    '''expresion : DECIMAL incdec'''
    t[0] = Primitivos(TIPO.DECIMAL, t[1], t[2], t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_cadena(t):
    '''expresion : CADENA'''
    t[0] = Primitivos(TIPO.CADENA, str(t[1]).replace('\\n', '\n'), None, t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_caracter(t):
    '''expresion : CHARACTER'''
    t[0] = Primitivos(TIPO.CHARACTER, str(t[1]).replace('\\n', '\n'), None, t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_booleano_true(t):
    'expresion : RTRUE'
    t[0] = Primitivos(TIPO.BOOLEANO, True,  None, t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_booleano_false(t):
    'expresion : RFALSE'
    t[0] = Primitivos(TIPO.BOOLEANO, False,  None, t.lineno(1), find_column(input, t.slice[1]))


#-----------------------Sentencias de Control-----------------------#
#--------------------------------If---------------------------------#
def p_if(t):
    'if : RIF PARA expresion PARC LLAVEA instrucciones LLAVEC'
    #print('Sentencia if por la expresion: ' + str(t[3]))
    t[0] = If(t[3], t[6], None, None, t.lineno(1), find_column(input, t.slice[1]))

def p_if_else(t):
    'if : RIF PARA expresion PARC LLAVEA instrucciones LLAVEC RELSE LLAVEA instrucciones LLAVEC'
    #print('Sentencia if con la expresion: ' + str(t[3]) + ' con opcion a else')
    t[0] = If(t[3], t[6], t[10], None, t.lineno(1), find_column(input, t.slice[1]))

def p_if_anidado(t):
    'if : RIF PARA expresion PARC LLAVEA instrucciones LLAVEC RELSE if'
    #print('Sentencia if con expresion: ' + str(t[3]) + ' seguido de if anidado')
    t[0] = If(t[3], t[6], None, t[9], t.lineno(1), find_column(input, t.slice[1]))


#--------------------Sentencias de Transferencia--------------------#
#-------------------------------Break-------------------------------#
# def p_break(t):
#     '''
#     break : RBREAK ptc
#     '''
#     #print('Se reconocio un break')
#     t[0] = t[1]

# def p_break1(t):
#     'break : '
#     t[0] = None


#-----------------------------Imprimir------------------------------#
def p_imprimir(t):
    'imprimir : RPRINT PARA expresion PARC'
    #print('Se ejecuto *print* ')# + str(t[3])) ###Revisar
    t[0] = Imprimir(t[3], t.lineno(1), find_column(input, t.slice[1]))


import ply.yacc as yacc
parser = yacc.yacc()

input = ''

def getErrores():
    return errores

def parse(inp) : #04/06/2021 <----------------Repasasr
    global errores
    global lexer
    global parser
    errores = []
    lexer = lex.lex()
    parser = yacc.yacc()
    global input
    input = inp
    return parser.parse(inp)

#INTERFAZ -- Debe estar en la interfaz

f = open("./entrada.txt", "r")
entrada = f.read()

from TS.Arbol import Arbol
from TS.TablaSimbolos import TablaSimbolos

instrucciones = parse(entrada) #ARBOL AST -- Aqui se creo
ast = Arbol(instrucciones)
TSGlobal = TablaSimbolos()
ast.setTSglobal(TSGlobal)
for error in errores: #CAPTURA DE ERRORES LEXICOS Y SINTACTICOS
    ast.getExcepciones().append(error)
    ast.updateConsola(error.toString())

for instruccion in ast.getInstrucciones(): # REALIZAR LAS ACCIONES
    value = instruccion.interpretar(ast,TSGlobal)
    if isinstance(value, Excepcion) :
        ast.getExcepciones().append(value)
        ast.updateConsola(value.toString())

print(ast.getConsola())