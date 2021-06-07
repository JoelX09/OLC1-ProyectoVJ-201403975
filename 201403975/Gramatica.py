'''
Gramatica Proyecto
Vacaciones Junio 2021
'''

# errores = []

from sys import stdout


reservadas = {
    'int'       : 'RINT',
    'double'    : 'RDOUBLE',
    'boolean'   : 'RBOOLEAN',
    'char'      : 'RCHAR',
    'string'    : 'RSTRING',
    'true'      : 'RTRUE',
    'false'     : 'RFALSE',
    'var'       : 'RVAR',
    'null'      : 'RNULL',
    'new'       : 'RNEW',
    'if'        : 'RIF',
    'else'      : 'RELSE',
    'switch'    : 'RSWITCH',
    'case'      : 'RCASE',
    'default'   : 'RDEFAULT',
    'while'     : 'RWHILE',
    'for'       : 'RFOR',
    'break'     : 'RBREAK',
    'continue'  : 'RCONTINUE',
    'return'    : 'RRETURN',
    'main'      : 'RMAIN',
    'print'     : 'RPRINT'
}

tokens  = [
    'PTCOMA',
    'INC',
    'DEC',
    'MAS',
    'MENOS',
    'POR',
    'DIV',
    'POT',
    'MOD',
    'IGUALIGUAL',
    'DIFERENTE',
    'IGUAL',
    'NEGACION',
    'MAYORIGUAL',
    'MAYORQUE',
    'MENORIGUAL',
    'MENORQUE',
    'SOR',
    'SAND',
    'PARA',
    'PARC',
    'CORA',
    'CORC',
    'LLAVEA',
    'LLAVEC',
    'DOSPT',
    'ENTERO',
    'DECIMAL',
    'CADENA',
    'CARACTER',
    'ID'
] + list(reservadas.values())

# Tokens
t_PTCOMA        = r';'
t_INC           = r'\+\+'
t_MAS           = r'\+'
t_DEC           = r'--'
t_MENOS         = r'-'
t_POT           = r'\*\*'
t_POR           = r'\*'
t_DIV           = r'/'
t_MOD           = r'%'
t_IGUALIGUAL    = r'=='
t_DIFERENTE     = r'=!'
t_IGUAL         = r'='
t_NEGACION      = r'!'
t_MAYORIGUAL    = r'>='
t_MAYORQUE      = r'>'
t_MENORIGUAL    = r'<='
t_MENORQUE      = r'<'
t_SOR           = r'\|\|'
t_SAND          = r'&&'
t_PARA          = r'\('
t_PARC          = r'\)'
t_CORA          = r'\['
t_CORC          = r']'
t_LLAVEA        = r'{'
t_LLAVEC        = r'}'
t_DOSPT         = r':'

def t_DECIMAL(t):
    r'\d+\.\d+' #expresiones regulares en yacc \d
    try:
        t.value = float(t.value)
    except ValueError:
        print("El valor es demasiado grande '%d'" % t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large '%d'" % t.value)
        t.value = 0
    return t

def t_CADENA(t):
    r'(\".*?\")'
    t.value = t.value[1:-1] # remuevo las comillas
    return t

def t_CARACTER(t):
    r'(\'.*?\')'
    t.value = t.value[1:-1] 
    return t

def t_ID(t):
     r'[a-zA-Z][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID') #Verifica si no es una reservada y si no se queda como ID
     return t

# def t_COMENTARIO_MULTIPLE(t):
#     r'\#\*.*\*\#'
#     print("Se reconocio comentario multiple: " + str(t.value))
#     t.lexer.lineno += 1

# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'\#.*\n'
    print("Se reconocio comentario simple: " + str(t.value))
    t.lexer.lineno += 1

#Caracteres ignorados
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno = t.value.count("\n")

def t_error(t): #LEXICOS
    print('caracter no reconocido: ' + str(t.value[0]))
    # almacenamiento de errores lexicos
    # errores.append(Excepcion("Lexico","Error léxico." + t.value[0] , t.lexer.lineno, find_column(input, t)))
    t.lexer.skip(1)

# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# Construyendo el analizador lexico
import ply.lex as lex
lexer = lex.lex()

# Definición de la gramática

# Presedencia
precedence = (
    ('right', 'UMENOS'),
    ('left', 'POR', 'DIV', 'MOD'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'IGUALIGUAL', 'DIFERENTE', 'MAYORQUE', 'MAYORIGUAL', 'MENORQUE', 'MENORIGUAL'),
    ('right', 'NEGACION'),
    ('left', 'SAND'),
    ('left', 'SOR')
)

def p_init(t) :
    'init            : instrucciones'
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

def p_inc_dec(t):
    '''
    incdec : INC
            | DEC
    '''
    t[0] = str(t[1])
    print('Se reconocio un dec o inc')

def p_inc_dec1(t):
    'incdec : '


def p_break(t): # Mover a sentencias de transferencia
    '''
    break : RBREAK ptc
    '''
    t[0] = str(t[1])
    print('Se reconocio un break')

def p_break1(t): # Mover a sentencias de transferencia
    'break : '

def p_instruccion_menu(t):
    'instruccion : menu'

def p_instruccion_imprimir(t):
    'instruccion : imprimir'

def p_instruccion_if(t):
    'instruccion : if'

def p_instruccion_switch(t):
    'instruccion : switch'

def p_instruccion_while(t):
    'instruccion : while'

def p_instruccion_for(t):
    'instruccion : for'

def p_instruccion_variables(t):
    'instruccion : variables'


#-----------------------------Variables-----------------------------#
def p_variables0(t):
    'variables : RVAR ID ptc'
    print('Se declaro la variable ' + str(t[2]))

def p_variables1(t):
    'variables : RVAR ID IGUAL expresion ptc' # Podria juntarlo con los de abajo
    print('Se declaro la variable ' + str(t[2]) + ' con el valor ' + str(t[4]))
    t[0]=t[4]

def p_variables2(t):
    'variables : RVAR ID IGUAL casteo ptc'
    print('Se declaro la variable ' + str(t[2]) + ' con el valor casteado ' + str(t[4]))
    t[0]=t[4]

def p_variables3(t):
    'variables : ID IGUAL expresion ptc'
    print('A la variable ' + str(t[1]) + ' se le asigno el valor ' + str(t[3]))
    t[0]=t[3]

def p_variables4(t):
    'variables : ID IGUAL casteo ptc'
    print('A la variable ' + str(t[1]) + ' se le asigno el valor casteado ' + str(t[3]))
    t[0]=t[3]

def p_variables5(t):
    'variables : ID IGUAL RNULL ptc'
    print('A la variable ' + str(t[1]) + ' se le asigno el valor ' + str(t[3]))

def p_variables6(t):
    'variables : ID incdec ptc'
    print('Se inc o dec la variable ' + t[1])
    if t[2]!= None:
        t[0]= str(t[1])+str(t[2])
    else:
        t[0]= str(t[1])

#------------------------------Casteo-------------------------------#
def p_casteo(t):
    'casteo : PARA tipo PARC expresion'
    print('Se casteo a ' + str(t[2]) + ' la expresion ' + str(t[4]))
    t[0] = t[4]

def p_tipo(t):
    '''tipo : RINT
            | RDOUBLE
            | RCHAR
            | RSTRING
    '''
    t[0] = str(t[1])


#----------------------------Expresiones----------------------------#
def p_expresion_binaria(t):
    '''
    expresion : expresion MAS expresion
            | expresion MENOS expresion
            | expresion POR expresion
            | expresion DIV expresion
            | expresion POT expresion
            | expresion MOD expresion
            | expresion IGUALIGUAL expresion
            | expresion MAYORQUE expresion
            | expresion MAYORIGUAL expresion
            | expresion MENORQUE expresion
            | expresion MENORIGUAL expresion
            | expresion DIFERENTE expresion
            | expresion SAND expresion
            | expresion SOR expresion
    '''
    t[0] = str(t[1]) + str(t[2]) + str(t[3]) 
    

def p_expresion_unaria_negativo(t):
    '''
    expresion : MENOS expresion %prec UMENOS
    '''
    t[0] = '-' + str(t[2])

def p_expresion_unaria_negacion(t):
    '''
    expresion : NEGACION expresion 
    '''
    t[0] = str(t[1]) + str(t[2])

def p_expresion_agrupacion(t):
    '''
    expresion : PARA expresion PARC
    '''
    t[0] = '(' + str(t[2]) + ')'

def p_expresion_primitivo_string(t):
    '''
    expresion : CADENA
            | CARACTER
            | RTRUE
            | RFALSE
    '''
    t[0] = str(t[1])

def p_expresion_primitivo_numero(t):
    '''
    expresion : ENTERO incdec
            | DECIMAL incdec
            | ID incdec
            | accesoArreglo incdec
    '''
    if t[2] != None:
        t[0] = str(t[1]) + str(t[2])
    else:
        t[0] = str(t[1])


#-----------------------------Arreglos------------------------------#
def p_acceso_arreglo(t):
    'accesoArreglo : ID listapos'
    dimensiones = ''
    for i in t[2]:
        dimensiones+=str(i)
    t[0] = str(t[1])+dimensiones


def p_lista_dimensiones0(t) :
    'listapos : listapos pos'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]

def p_lista_dimensiones1(t) :
    'listapos : pos'
    if t[1] == "":
        t[0] = []
    else:    
        t[0] = [t[1]]

def p_lista_dimensiones2(t):
    'pos : CORA expresion CORC'
    t[0] = '[' + str(t[2]) + ']'


#-----------------------Sentencias de Control-----------------------#

#--------------------------------If---------------------------------#
def p_if1(t):
    'if : RIF PARA expresion PARC LLAVEA opciones LLAVEC'
    print('Sentencia if por la expresion: ' + str(t[3]))

def p_if2(t):
    'if : RIF PARA expresion PARC LLAVEA opciones LLAVEC RELSE LLAVEA opciones LLAVEC'
    print('Sentencia if con la expresion: ' + str(t[3]) + ' con opcion a else')

def p_if3(t):
    'if : RIF PARA expresion PARC LLAVEA opciones LLAVEC RELSE if'
    print('Sentencia if con expresion: ' + str(t[3]) + ' seguido de if anidado')


def p_break_ciclos1(t):
    'opciones : opciones opcion'

def p_break_ciclos2(t):
    'opciones : opcion'

def p_break_ciclos3(t):
    '''
    opcion : instrucciones
            | break
    '''

#------------------------------Switch-------------------------------#
def p_switch1(t):
    'switch : RSWITCH PARA expresion PARC LLAVEA caselist default LLAVEC'
    print("Switch recibe la expresion: " + str(t[3]) + ' y tiene case y default')

def p_switch2(t):
    'switch : RSWITCH PARA expresion PARC LLAVEA caselist LLAVEC'
    print("Switch recibe la expresion: " + str(t[3]) + ' y tiene case')

def p_switch3(t):
    'switch : RSWITCH PARA expresion PARC LLAVEA default LLAVEC'
    print("Switch recibe la expresion: " + str(t[3]) + ' y tiene default')

def p_cases1(t):
    'caselist : caselist case'

def p_cases2(t):
    'caselist : case'

def p_case(t):
    'case : RCASE expresion DOSPT instrucciones break'
    print("Case evaluado con la expresion: " + str(t[2]))

def p_defaul(t):
    'default : RDEFAULT DOSPT instrucciones break'
    print("Se evaluo el default")


#-------------------------------While-------------------------------#
def p_while1(t):
    'while : RWHILE PARA expresion PARC LLAVEA opciones LLAVEC'
    print('Sentencia while por la expresion: ' + str(t[3]))


#--------------------------------for--------------------------------#
def p_for1(t):
    'for : RFOR PARA variables expresion PTCOMA variables PARC LLAVEA opciones LLAVEC'
    print("Sentencia for declarada con los parametros: " + str(t[3]) + ", " + str(t[4]) + ", " + str(t[6]) + ", ")

# def p_for2(t):
#     'decAs : variables'

# def p_for3(t):
#     'cond : expresion'

# def p_for4(t):
#     'act : variables'


#-------------------------------Main--------------------------------#
def p_menu(t):
    'menu : RMAIN PARA PARC LLAVEA instrucciones LLAVEC'
    print('Se ejecuto el main')


#-----------------------------Imprimir------------------------------#
def p_print(t):
    'imprimir : RPRINT PARA expresion PARC ptc'
    print('Se ejecuto *print* ' + str(t[3]))


#---------------------------Fin Gramatica---------------------------#
def p_error(t):
    print('Error sintactico en: ' + str(t.value))
    # almacenamiento de errores sintacticos

import ply.yacc as yacc
parser = yacc.yacc()

f = open("./entrada.txt", "r")
input = f.read()
print(input)
parser.parse(input)
print("Archivo ejecutado correctamente :D")