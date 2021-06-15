class Errores():

    def generarReporte(errores):
        html = """<!DOCTYPE HTML5>  
<html>
<head>
    <title>OLC1 - Proyecto - JPR</title>
    <meta charset=\"utf-8\">
    <meta name=\"author\" content=\"\">
    <meta name=\"description\" content=\"OLC1 - Proyecto 1\">
</head>
<body><center>
    <table border=\"1\">
    <caption>Reporte de Errores</caption>
    <tr>
        <th>#</th>
        <th>Tipo de Error</th>
        <th>Descripcion</th>
        <th>Linea</th>
        <th>Columna</th>
    </tr>"""
        
        for i in range(0, len(errores)):
            html += """     <tr>
        <th>""" + str(i+1) + """</th>
        <th>""" + str(errores[i].tipo) + """</th>
        <th>""" + str(errores[i].descripcion) + """</th>
        <th>""" + str(errores[i].fila) + """</th>
        <th>""" + str(errores[i].columna) + """</th>
    </tr>
"""
        
        html += """     </table>
</center></body>
</html>"""

        file = open("D:\\Escritorio\\Errores.html", "w+")
        file.write(html)
        file.close()