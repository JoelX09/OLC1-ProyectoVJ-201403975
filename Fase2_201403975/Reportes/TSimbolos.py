import os

class TSimbolos():

    def generarReporte(TS):
        html = """<!DOCTYPE HTML5>  
<html>
<head>
    <title>JPR - Tabla de Simbolos</title>
    <meta charset=\"utf-8\">
    <meta name=\"author\" content=\"\">
    <meta name=\"description\" content=\"OLC1 - Proyecto 1\">
</head>
<body><center>
    <table border=\"1\">
    <caption>Tabla de Simbolos</caption>
    <tr>
        <th>Identificador</th>
        <th>Tipo Simbolo</th>
        <th>Tipo</th>
        <th>Entorno</th>
        <th>Valor</th>
        <th>Linea</th>
        <th>Columna</th>
    </tr>"""
        
        for i in TS:
            html += """     <tr>
        <th>""" + str(TS[i].getIdentificador()) + """</th>
        <th>""" + str(TS[i].getTipoSimbolo()) + """</th>
        <th>""" + str(TS[i].getTipo()) + """</th>
        <th>""" + str(TS[i].getEntorno()) + """</th>
        <th>""" + str(TS[i].getValor()) + """</th>
        <th>""" + str(TS[i].getFila()) + """</th>
        <th>""" + str(TS[i].getColumna()) + """</th>
    </tr>
"""
        
        html += """     </table>
</center></body>
</html>"""

        try:
            os.stat("./Salidas")
        except:
            os.mkdir("./Salidas")

        file = open("./Salidas/TS.html", "w+")
        file.write(html)
        file.close()