from Abstract.NodoAST import NodoAST
from Abstract.Instruccion import Instruccion
from TS.Tipo import TIPO
from tkinter import *

class Read(Instruccion):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.CADENA

    def interpretar(self, tree, table):
        #print(tree.getConsola()) #IMPRIME LA CONSOLA
        #print("Ingreso a un READ. Ingrese el valor")
        #tree.setConsola("")     #RESETEA LA CONSOLA
        # ESTO SOLO ES DE EJEMPLO
        # lectura = input() # OBTENERME EL VALOR INGRESADO
        # return lectura
        
        self.w=Entrada(tree.ventana, tree.textoRead)
        tree.ventana.wait_window(self.w.top)

        return self.w.value

    def getNodo(self):
        nodo = NodoAST("READ")
        return nodo


class Entrada(object):
    def __init__(self, ventana, texto):
        top=self.top=Toplevel(ventana)
        top.title('Entrada')
        top.geometry("500x250")
        self.l=Label(top,text=str(texto))
        self.l.pack()
        self.e=Entry(top)
        self.e.pack()
        self.b=Button(top,text='Ok',command=self.continuar)
        self.b.pack()

    def continuar(self):
        self.value = self.e.get()
        self.top.destroy()