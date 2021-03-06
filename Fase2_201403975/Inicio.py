from tkinter import Button, PhotoImage, Canvas, Frame, Label, Tk, Menu, messagebox, scrolledtext, filedialog
from tkinter import BOTH, INSERT, END, LEFT
import os, re

root = Tk()

# Configuraciones de la Ventara principal
root.title('JPR')
root.geometry("1000x600")
root.iconbitmap('icon/document.ico')

# Opciones del Menu, Autor PUAC

# Path del archivo en memoria, Autor PUAC
archivo = ""   

# Nuevo archivo, Autor PUAC
def nuevo():
    global archivo
    editor.delete(1.0, END)
    consola.delete(1.0, END)
    archivo = ""

# Abrir archivo, Autor PUAC
def abrir():
    global archivo
    archivo = filedialog.askopenfilename(title = "Abrir Archivo", initialdir = "D:/", filetypes = (("JPR","*.jpr"),("all files","*.*")))

    entrada = open(archivo, encoding='utf-8')
    content = entrada.read()

    editor.delete(1.0, END)
    consola.delete(1.0, END)
    #editor.insert(1.0, content)
    #entrada.close()
    #lineas()
    #val = editor.get("1.0", END)
    #editor.delete(1.0, END)
    for s in recorrerInput(content):
        editor.insert(INSERT, s[1], s[0])
    entrada.close()
    lineas()

# Guardar Archivo, Autor PUAC
def guardarArchivo(): 
    val = editor.get("1.0", END)
    editor.delete(1.0, END)
    for s in recorrerInput(val):
        editor.insert(INSERT, s[1], s[0])
    global archivo
    if archivo == "":
        guardarComo()
    else:
        guardarc = open(archivo, "w", encoding='utf-8')
        guardarc.write(editor.get(1.0, END))
        guardarc.close()

# Guardar como, Autor PUAC
def guardarComo():
    val = editor.get("1.0", END)
    editor.delete(1.0, END)
    for s in recorrerInput(val):
        editor.insert(INSERT, s[1], s[0])
    global archivo
    guardar = filedialog.asksaveasfilename(title = "Guardar Archivo", initialdir = "D:/", filetypes = (("JPR","*.jpr"),("all files","*.*")))
    fguardar = open(guardar, "w+", encoding='utf-8')
    fguardar.write(editor.get(1.0, END))
    fguardar.close()
    archivo = guardar

# Abrir reporte de errores, Autor PUAC
def openErrores():
    dirname = os.path.dirname(__file__)
    direcc = os.path.join(dirname, 'Salidas/Errores.html')
    os.startfile(direcc)

# Abrir reporte de AST, Autor PUAC
def openAST():
    dirname = os.path.dirname(__file__)
    # direcc = os.path.join(dirname, 'Salidas/AST.pdf')
    # os.startfile(direcc)

    import subprocess
    chrome_path = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
    p = subprocess.Popen([chrome_path, dirname + "/Salidas/AST.pdf"]) 
    p.wait() #This waits for the process to clos

def openUsuario():
    dirname = os.path.dirname(__file__)
    direcc = os.path.join(dirname, 'Manuales/Usuario.pdf')
    os.startfile(direcc)

def openTecnico():
    dirname = os.path.dirname(__file__)
    direcc = os.path.join(dirname, 'Manuales/Tecnico.pdf')
    os.startfile(direcc)

def openGramatica():
    dirname = os.path.dirname(__file__)
    direcc = os.path.join(dirname, 'Manuales/Gramatica.pdf')
    os.startfile(direcc)

# Abrir reporte TS, Autor PUAC
def openTS():
    dirname = os.path.dirname(__file__)
    direcc = os.path.join(dirname, 'Salidas/TS.html')
    os.startfile(direcc)

# Ejecucion del analizador
def ejecutar():
    #f = open("./entrada.txt", "r")
    #entrada = f.read()
    consola.delete(1.0, END)
    entrada = editor.get("1.0", END)
    editor.delete(1.0, END)
    for s in recorrerInput(entrada):
        editor.insert(INSERT, s[1], s[0])

    from TS.Arbol import Arbol
    from TS.TablaSimbolos import TablaSimbolos
    from Reportes.Errores import Errores
    from Reportes.TSimbolos import TSimbolos
    from Gramatica import parse, getErrores, crearNativas
    from Instrucciones.Declaracion import Declaracion
    from Instrucciones.Asignacion import Asignacion
    from TS.Excepcion import Excepcion
    from Instrucciones.Break import Break
    from Instrucciones.Continue import Continue
    from Instrucciones.Return import Return
    from Instrucciones.Main import Main
    from Instrucciones.Funcion import Funcion
    from Abstract.NodoAST import NodoAST
    from Instrucciones.DeclaracionT1 import DeclaracionT1
    from Instrucciones.Tipo2 import DeclaracionT2
    from Instrucciones.Tipo3 import DeclaracionT3
    from Instrucciones.ModificarArreglo import ModificarArreglo

    instrucciones = parse(entrada) #ARBOL AST -- Aqui se creo
    ast = Arbol(instrucciones)
    ast.ventana = root
    ast.salida = consola
    TSGlobal = TablaSimbolos()
    ast.setTSglobal(TSGlobal)
    crearNativas(ast)
    for error in getErrores(): #CAPTURA DE ERRORES LEXICOS Y SINTACTICOS
        ast.getExcepciones().append(error)
        ast.updateConsola(error.toString())

    for instruccion in ast.getInstrucciones(): # Primera pasada
        ast.entorno = "Global"
        if isinstance(instruccion, Funcion):
            ast.addFuncion(instruccion)     # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)
        if isinstance(instruccion, Declaracion) or isinstance(instruccion, Asignacion) or isinstance(instruccion, DeclaracionT1) or isinstance(instruccion, ModificarArreglo) or isinstance(instruccion, DeclaracionT2) or isinstance(instruccion, DeclaracionT3):
            value = instruccion.interpretar(ast,TSGlobal)
            if isinstance(value, Excepcion) :
                ast.getExcepciones().append(value)
                ast.updateConsola(value.toString())
            if isinstance(value, Break): 
                err = Excepcion("Semantico", "Sentencia BREAK fuera de ciclo", instruccion.fila, instruccion.columna)
                ast.getExcepciones().append(err)
                ast.updateConsola(err.toString())

    contador = 0
    for instruccion in ast.getInstrucciones(): # Segunda pasada
        ast.entorno = "Global"
        if isinstance(instruccion, Main):
            contador += 1
            if contador == 2: # Duplicidad
                err = Excepcion("Semantico", "Existe mas de una funcion Main", instruccion.fila, instruccion.columna)
                ast.getExcepciones().append(err)
                ast.updateConsola(err.toString())
                break
            value = instruccion.interpretar(ast,TSGlobal)
            if isinstance(value, Excepcion) :
                ast.getExcepciones().append(value)
                ast.updateConsola(value.toString())
            if isinstance(value, Break): 
                err = Excepcion("Semantico", "Sentencia BREAK fuera de ciclo", instruccion.fila, instruccion.columna)
                ast.getExcepciones().append(err)
                ast.updateConsola(err.toString())
            if isinstance(value, Continue): 
                err = Excepcion("Semantico", "Sentencia CONTINUE fuera de ciclo", instruccion.fila, instruccion.columna)
                ast.getExcepciones().append(err)
                ast.updateConsola(err.toString())
            if isinstance(value, Return): 
                err = Excepcion("Semantico", "Sentencia RETURN fuera de ciclo", instruccion.fila, instruccion.columna)
                ast.getExcepciones().append(err)
                ast.updateConsola(err.toString())

    for instruccion in ast.getInstrucciones():  # Tercera pasada  
        if not (isinstance(instruccion, Main) or isinstance(instruccion, Declaracion) or isinstance(instruccion, Asignacion) or isinstance(instruccion, Funcion) or isinstance(instruccion, DeclaracionT1) or isinstance(instruccion, ModificarArreglo) or isinstance(instruccion, DeclaracionT2) or isinstance(instruccion, DeclaracionT3)):
            err = Excepcion("Semantico", "Sentencias fuera de Main", instruccion.fila, instruccion.columna)
            ast.getExcepciones().append(err)
            ast.updateConsola(err.toString())

    Errores.generarReporte(ast.getExcepciones())
    TSimbolos.generarReporte(ast.getSimbolos())

    #print(ast.getConsola())
    consola.delete(1.0, END)
    consola.insert(1.0, ast.getConsola())

    init = NodoAST("RAIZ")
    instr = NodoAST("INSTRUCCIONES")

    for instruccion in ast.getInstrucciones():
        instr.agregarHijoNodo(instruccion.getNodo())

    init.agregarHijoNodo(instr)
    grafo = ast.getDot(init) #DEVUELVE EL CODIGO GRAPHVIZ DEL AST

    # dirname = os.path.dirname(__file__)
    # direcc = os.path.join(dirname, 'ast.dot')
    arch = open("./Salidas/AST.dot", "w+", encoding="utf-8")
    arch.write(grafo)
    arch.close()

    #Path
    os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'
    os.system('dot -T pdf -o ./Salidas/AST.pdf ./Salidas/AST.dot')

# Menu desplegable
menu = Menu(root)
root.config(menu=menu)

menuArchivo = Menu(menu)
menu.add_cascade(label='Archivo', menu=menuArchivo)
menuArchivo.add_command(label='Nuevo', command=nuevo)
menuArchivo.add_command(label='Abrir', command=abrir)
menuArchivo.add_command(label='Guardar', command=guardarArchivo)
menuArchivo.add_command(label='Guardar Como', command=guardarComo)

menuReportes = Menu(menu)
menu.add_cascade(label='Reportes', menu=menuReportes)
menuReportes.add_command(label='Errores', command=openErrores)
menuReportes.add_command(label='AST', command=openAST)
menuReportes.add_command(label='Tabla de Simbolos', command=openTS)

menuAyuda = Menu(menu)
menu.add_cascade(label='Ayuda', menu=menuAyuda)
menuAyuda.add_command(label='Manual de Usuario', command= openUsuario)
menuAyuda.add_command(label='Manual Tecnico', command= openTecnico)
menuAyuda.add_command(label='Gramatica', command= openGramatica)
menuAyuda.add_command(label='Acerca de...', command= lambda: messagebox.showinfo("Informaci??n", "Joel Obdulio Xicar?? R??os\n201403975"))

# Funcion para obtener palabrvas reservadas, signos, numeros, etc, Autor PUAC
def recorrerInput(i):
    #i += "\n"
    lista = []
    val = ''
    counter = 0

    while counter < len(i):
        if re.search(r"[a-zA-Z_0-9]", i[counter]):
            val += i[counter]

        elif i[counter] == "#":
            if len(val) != 0:
                l = []
                l.append("variable")
                l.append(val)
                lista.append(l)
                val = ''
            val = i[counter]
            counter += 1
            if i[counter] == "*":
                val += i[counter]
                counter += 1
                while counter < len(i):
                    if i[counter] == "#":
                        val += i[counter]
                        l = []
                        l.append("comentario")
                        l.append(val)
                        lista.append(l)
                        val = ''
                        break
                    val += i[counter]
                    counter += 1
            else:
                while counter < len(i):
                    if i[counter] == "\n":
                        val += i[counter]
                        l = []
                        l.append("comentario")
                        l.append(val)
                        lista.append(l)
                        val = ''
                        break
                    elif counter == len(i)-1:
                        val += i[counter]
                        l = []
                        l.append("comentario")
                        l.append(val)
                        lista.append(l)
                        val = ''
                        break
                    val += i[counter]
                    counter += 1
                    
        elif i[counter] == "\"":
            if len(val) != 0:
                l = []
                l.append("variable")
                l.append(val)
                lista.append(l)
                val = ''
            val = i[counter]
            counter += 1
            while counter < len(i):
                if i[counter] == "\"":
                    val += i[counter]
                    l = []
                    l.append("string")
                    l.append(val)
                    lista.append(l)
                    val = ''
                    break
                val += i[counter]
                counter += 1

        elif i[counter] == "\'":
            if len(val) != 0:
                l = []
                l.append("variable")
                l.append(val)
                lista.append(l)
                val = ''
            val = i[counter]
            counter += 1
            while counter < len(i):
                if i[counter] == "\'":
                    val += i[counter]
                    l = []
                    l.append("string")
                    l.append(val)
                    lista.append(l)
                    val = ''
                    break
                val += i[counter]
                counter += 1
                
        else:
            if len(val) != 0:
                l = []
                l.append("variable")
                l.append(val)
                lista.append(l)
                val = ''
            l = []
            l.append("signo")
            l.append(i[counter])
            lista.append(l)
        counter +=1
        
    for s in lista:
        if s[1].lower() == 'new' or s[1].lower() == 'int' or s[1].lower() == 'double' or s[1].lower() == 'boolean' or s[1].lower() == 'string' or s[1].lower() == 'char' or s[1].lower() == 'func' or s[1].lower() == 'var' or s[1].lower() == 'true' or s[1].lower() == 'false' or s[1].lower() == 'print' or s[1].lower() == 'main' or s[1].lower() == 'null' or s[1].lower() == 'if' or s[1].lower() == 'else' or s[1].lower() == 'switch' or s[1].lower() == 'case' or s[1].lower() == 'default' or s[1].lower() == 'while' or s[1].lower() == 'for' or s[1].lower() == 'break' or s[1].lower() == 'continue' or s[1].lower() == 'return':
            s[0] = 'reservada'
        elif re.match(r"[0-9]+(\.[0-9])?", s[1]):
            s[0] = 'numeros'
    return lista

# Actualizar No. de lineas en el editor, Autor PUAC
def lineas(*args): 
    lines.delete("all")

    cont = editor.index("@1,0")
    while True :
        dline= editor.dlineinfo(cont)
        if dline is None: 
            break
        y = dline[1]
        strline = str(cont).split(".")[0]
        lines.create_text(2,y,anchor="nw", text=strline, font = ("Console", 12))
        cont = editor.index("%s+1line" % cont)

# Posicion del cursor, Autor PUAC
def posicion(event):
    labelfc.config(text = "Linea: " + str(editor.index(INSERT)).replace("."," | Columna: ") )

# Creando frames de la Ventana principal
frameTop = Frame(root)
frameMiddle = Frame(root)
frameBottom = Frame(root)

# Colocando los frames en la ventana
frameTop.pack(side="top", fill = BOTH)
frameMiddle.pack(fill = BOTH, expand = True)
frameBottom.pack(side="bottom", fill = BOTH, expand = True)

# Creando elementos visuales de la Ventana principal
inconoEjecutar = PhotoImage(file='icon/play.png')
btnEjecutar = Button(frameTop, text="Interpretar" , image= inconoEjecutar , compound=LEFT, command=ejecutar)
btnDebugger = Button(frameTop, text="Debugger")
labelfc = Label(frameTop, text='Linea: 1 | Columna: 1')  
lines = Canvas(frameMiddle, width=40, height=8, bg="LightCyan2")
editor = scrolledtext.ScrolledText(frameMiddle, undo=True, width=250, height=8, font=("Consolas", 12))
consola = scrolledtext.ScrolledText(frameBottom, width=30, height=8, font=("Consolas", 12))

# Asignando los elementos a cada frame
btnEjecutar.pack(side='left')
btnDebugger.pack(side='left', padx=10)
labelfc.pack(expand='no', fill=None, side='right', anchor='se', padx=20)
lines.pack(side="left", fill=BOTH, expand=True, padx=12, pady=12)
editor.pack(fill=BOTH, expand = True , padx= 12 , pady= 12)
consola.pack(fill = BOTH, expand = True, padx = 12 , pady = 12)

# Cambio de colores
editor.tag_config('reservada', foreground='blue')
editor.tag_config('string', foreground='orange')
editor.tag_config('numeros', foreground='purple')
editor.tag_config('comentario', foreground='gray')

# Acciones que hacen que se actualice la fila y columna, Autor PUAC
editor.bind('<Return>', lineas)
editor.bind('<BackSpace>', lineas)
editor.bind('<<Change>>', lineas)
editor.bind('<Configure>', lineas)
editor.bind('<Motion>', lineas)
editor.bind('<KeyPress>', posicion)
editor.bind('<Button-1>', posicion)

root.mainloop()