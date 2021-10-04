import psycopg2

from flask import Flask
from flask_jsonpify import jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
connection = "host=%s port=%s user=%s password=%s dbname=%s" % ('localhost', 5432, 'william', 201909103, 'practica')

try:
    conn = psycopg2.connect(connection)
    cur = conn.cursor()

    @app.route("/")
    def home_view():
        return "<h1>201909103</h1>"

    @app.route("/ejecutar")
    def ejecutar():    
        cur.execute('SELECT * FROM movies')
        rows = cur.fetchall()
        print(rows)
        return jsonify(rows)

    @app.route("/consulta1")
    def consulta1():    
        cur.execute('SELECT Nombre, Cantidad FROM PELICULA WHERE Nombre=\'SUGAR WONKA\';')
        cadena="<TABLE BORDER><TR><TH>No.</TH><TH>NombrePelicula</TH><TH>Cantidad</TH></TR>"
        rows = cur.fetchall()
        for row in range(len(rows)):
            cadena+="<TR><TD>"+str(row+1)
            cadena+="</TD><TD>"+str(rows[row][0])
            cadena+="</TD><TD>"+str(rows[row][1])
            cadena+="</TD></TR>"
        cadena+="</TABLE>"
        return cadena

    @app.route("/consulta2")
    def consulta2():    
        cur.execute('SELECT DISTINCT CLIENTE.Nombre, CLIENTE.Apellido,'+ 
					' (SELECT SUM(CAST(RENTA1.MontoPagar AS DECIMAL)) FROM RENTA RENTA1 INNER JOIN CLIENTE CLIENTE1'+
					' ON RENTA1.Cliente = CLIENTE1.Correo WHERE CLIENTE1.Correo=CLIENTE.Correo)as Monto'+ 
                    ' FROM CLIENTE INNER JOIN RENTA ON CLIENTE.Correo = RENTA.Cliente'+ 
                    ' WHERE CLIENTE.Rentas >39;')
        cadena="<TABLE BORDER><TR><TH>No.</TH><TH>Nombre</TH><TH>Apellido</TH><TH>Monto</TH></TR>"
        rows = cur.fetchall()
        for row in range(len(rows)):
            cadena+="<TR><TD>"+str(row+1)
            cadena+="</TD><TD>"+str(rows[row][0])
            cadena+="</TD><TD>"+str(rows[row][1])
            cadena+="</TD><TD>"+str(rows[row][2])
            cadena+="</TD></TR>"
        cadena+="</TABLE>"
        return cadena

    @app.route("/consulta3")
    def consulta3():    
        cur.execute('SELECT DISTINCT NombreCompleto FROM ACTOR WHERE (position(\'son\' in LOWER(Apellido))>0) ORDER BY NombreCompleto ASC;')
        cadena="<TABLE BORDER><TR><TH>No.</TH><TH>Nombre Completo</TH></TR>"
        rows = cur.fetchall()
        for row in range(len(rows)):
            cadena+="<TR><TD>"+str(row+1)
            cadena+="</TD><TD>"+str(rows[row][0])
            cadena+="</TD></TR>"
        cadena+="</TABLE>"
        return cadena

    @app.route("/consulta4")
    def consulta4():    
        cur.execute('SELECT PELICULA.Nombre, PELICULA.Descripcion, ACTOR.NombreCompleto, Pelicula.AnioLanzamiento'+
                    ' FROM PELICULA INNER JOIN ACTOR ON PELICULA.Nombre = ACTOR.Pelicula'+ 
                    ' WHERE( (position(\'crocodile\' in LOWER(PELICULA.Descripcion))>0) and'+
                    ' (position(\'shark\' in LOWER(PELICULA.Descripcion))>0) and'+
                    ' not ACTOR.NombreCompleto=\'-\')'+ 
                    ' ORDER BY ACTOR.Apellido ASC;')
        cadena="<TABLE BORDER><TR><TH>No.</TH><TH>Nombre Pelicula</TH><TH>Descripcion</TH><TH>Actor</TH><TH>Anio Lanzamiento</TH></TR>"
        rows = cur.fetchall()
        for row in range(len(rows)):
            cadena+="<TR><TD>"+str(row+1)
            cadena+="</TD><TD>"+str(rows[row][0])
            cadena+="</TD><TD>"+str(rows[row][1])
            cadena+="</TD><TD>"+str(rows[row][2])
            cadena+="</TD><TD>"+str(rows[row][3])
            cadena+="</TD></TR>"
        cadena+="</TABLE>"
        return cadena

    @app.route("/consulta5")
    def consulta5():    
        cur.execute('SELECT DISTINCT DIRECCION.Pais, CLIENTE.Nombre, CLIENTE.Apellido,'+
					' CONCAT(ROUND(((CLIENTE.Rentas)::DECIMAL*100 /'+
					' (SELECT SUM(Rentas) FROM CLIENTE CL  INNER JOIN DIRECCION DR'+
					' ON CL.idDireccion=DR.idDireccion'+
					' WHERE DR.Pais=DIRECCION.Pais)::DECIMAL)::DECIMAL, 2),\' %\') as porcentaje '+
                    ' FROM DIRECCION INNER JOIN CLIENTE ON DIRECCION.idDireccion = CLIENTE.idDireccion'+ 
                    ' WHERE CLIENTE.Rentas = (SELECT MAX (Rentas) FROM CLIENTE);')
        cadena="<TABLE BORDER><TR><TH>No.</TH><TH>Pais</TH><TH>Nombre</TH><TH>Apellido</TH><TH>Porcentaje</TH></TR>"
        rows = cur.fetchall()
        for row in range(len(rows)):
            cadena+="<TR><TD>"+str(row+1)
            cadena+="</TD><TD>"+str(rows[row][0])
            cadena+="</TD><TD>"+str(rows[row][1])
            cadena+="</TD><TD>"+str(rows[row][2])
            cadena+="</TD><TD>"+str(rows[row][3])
            cadena+="</TD></TR>"
        cadena+="</TABLE>"
        return cadena


    @app.route("/consulta6")
    def consulta6():    
        cur.execute('SELECT DISTINCT (SELECT COUNT(*) FROM CLIENTE) AS TOTAL_CLIENTES, D.Pais, D.Ciudad, CONCAT(ROUND(('+
                    ' SELECT COUNT(*)'+
                    ' FROM DIRECCION INNER JOIN CLIENTE ON DIRECCION.idDireccion = CLIENTE.idDireccion'+
                    ' WHERE DIRECCION.Pais=D.Pais AND DIRECCION.Ciudad=D.Ciudad'+
                    ' GROUP BY DIRECCION.Pais, DIRECCION.Ciudad)::DECIMAL*100 /'+
                    ' (SELECT COUNT(*)'+
                    ' FROM DIRECCION INNER JOIN CLIENTE ON DIRECCION.idDireccion = CLIENTE.idDireccion'+
                    ' WHERE DIRECCION.Pais=D.Pais'+
                    ' GROUP BY DIRECCION.Pais)::DECIMAL, 2), \' %\') as Porcentaje'+
                    ' FROM DIRECCION D ORDER BY D.Pais ASC;')
        cadena="<TABLE BORDER><TR><TH>No.</TH><TH>TotalClientes</TH> <TH>Pais</TH> <TH>Ciudad</TH> <TH>Porcentaje</TH></TR>"
        rows = cur.fetchall()

        #una limpieza de datos vacíos
        nuevo=[]
        for i in rows:
            if i[3] != "%" and i[3] != " %" and i[3] != "" and i[3] != "0.00 %" and i[3] != "null":
                nuevo.append(i)
        rows=nuevo

        for row in range(len(rows)):
            cadena+="<TR><TD>"+str(row+1)
            cadena+="</TD><TD>"+str(rows[row][0])
            cadena+="</TD><TD>"+str(rows[row][1])
            cadena+="</TD><TD>"+str(rows[row][2])
            cadena+="</TD><TD>"+str(rows[row][3])
            cadena+="</TD></TR>"
        cadena+="</TABLE>"
        return cadena

    @app.route("/consulta7")
    def consulta7():    
        cur.execute('SELECT DISTINCT DP.Pais, DP.Ciudad, (SELECT COUNT(*)'+
                    ' FROM RENTA'+
                    ' INNER JOIN CLIENTE ON RENTA.Cliente = CLIENTE.Correo'+
                    ' INNER JOIN DIRECCION ON CLIENTE.idDireccion = DIRECCION.idDireccion'+
                    ' WHERE DIRECCION.Pais=DP.Pais and DIRECCION.Ciudad=DP.Ciudad) AS Rentas,'+
                    ' (ROUND((SELECT COUNT(*)'+
                    ' FROM RENTA'+
                    ' INNER JOIN CLIENTE ON RENTA.Cliente = CLIENTE.Correo'+
                    ' INNER JOIN DIRECCION ON CLIENTE.idDireccion = DIRECCION.idDireccion'+
                    ' WHERE DIRECCION.Pais=DP.Pais and DIRECCION.Ciudad=DP.Ciudad)::DECIMAL /'+
                    ' (SELECT COUNT(*) FROM DIRECCION DCP WHERE DCP.Pais=DP.Pais GROUP BY DCP.Pais)::DECIMAL,2)'+
                    ' )AS Promedio FROM DIRECCION DP ORDER BY DP.Pais ASC, DP.Ciudad ASC;')
        cadena="<TABLE BORDER><TR><TH>No.</TH><TH>Pais</TH> <TH>Ciudad</TH> <TH>Rentas</TH> <TH>Promedio</TH></TR>"
        rows = cur.fetchall()
        for row in range(len(rows)):
            cadena+="<TR><TD>"+str(row+1)
            cadena+="</TD><TD>"+str(rows[row][0])
            cadena+="</TD><TD>"+str(rows[row][1])
            cadena+="</TD><TD>"+str(rows[row][2])
            cadena+="</TD><TD>"+str(rows[row][3])
            cadena+="</TD></TR>"
        cadena+="</TABLE>"
        return cadena

    @app.route("/consulta8")
    def consulta8():    
        cur.execute('SELECT DISTINCT DP.Pais, CONCAT(ROUND(('+
                    ' (SELECT COUNT(*)'+
                    ' FROM RENTA RENTA2'+
                    ' INNER JOIN CLIENTE CLIENTE2  ON RENTA2.Cliente = CLIENTE2.Correo'+
                    ' INNER JOIN PELICULA PELICULA2 ON RENTA2.Pelicula = PELICULA2.Nombre'+
                    ' INNER JOIN CATEGORIA CATEGORIA2 ON RENTA2.Pelicula = CATEGORIA2.Pelicula'+
                    ' INNER JOIN DIRECCION DIRECCION2 ON CLIENTE2.idDireccion = DIRECCION2.idDireccion'+
                    ' WHERE DIRECCION2.Pais=DP.Pais and CATEGORIA2.Nombre=\'Sports\' HAVING COUNT(*)>0)::DECIMAL*100 /'+
                    ' NULLIF((SELECT DISTINCT COUNT(*)'+
                    ' FROM RENTA RENTA1'+
                    ' INNER JOIN CLIENTE CLIENTE1  ON RENTA1.Cliente = CLIENTE1.Correo'+
                    ' INNER JOIN PELICULA PELICULA1 ON RENTA1.Pelicula = PELICULA1.Nombre'+
                    ' INNER JOIN CATEGORIA CATEGORIA1 ON RENTA1.Pelicula = CATEGORIA1.Pelicula'+
                    ' INNER JOIN DIRECCION DIRECCION1 ON CLIENTE1.idDireccion = DIRECCION1.idDireccion'+
                    ' WHERE DIRECCION1.Pais=DP.Pais'+
                    ' HAVING COUNT(*)>0)::DECIMAL,0)'+
                    ' ),2), \' %\') AS PROMEDIO_SPORTS'+
                    ' FROM DIRECCION DP ORDER BY DP.Pais ASC;')
        cadena="<TABLE BORDER><TR><TH>No.</TH><TH>Pais</TH> <TH>Porcentaje Sports</TH></TR>"
        rows = cur.fetchall()

        #una limpieza de datos vacíos
        nuevo=[]
        for i in rows:
            if i[1] != "%" and i[1] != " %" and i[1] != "" and i[1] != "0.00 %" and i[1] != "null":
                nuevo.append(i)
        rows=nuevo
        for row in range(len(rows)):
            cadena+="<TR><TD>"+str(row+1)
            cadena+="</TD><TD>"+str(rows[row][0])
            cadena+="</TD><TD>"+str(rows[row][1])
            cadena+="</TD></TR>"
        cadena+="</TABLE>"
        return cadena

    @app.route("/consulta9")
    def consulta9():    
        cur.execute('SELECT DISTINCT DP.Ciudad, (SELECT COUNT(*)'+
						' FROM RENTA'+ 
						' INNER JOIN CLIENTE ON RENTA.Cliente = CLIENTE.Correo'+
						' INNER JOIN PELICULA ON RENTA.Pelicula = PELICULA.Nombre'+
						' INNER JOIN DIRECCION ON CLIENTE.idDireccion = DIRECCION.idDireccion'+
						' WHERE (DIRECCION.Pais=\'United States\' or DIRECCION.Pais=\'Estados Unidos\') and'+
						' DIRECCION.Ciudad=DP.Ciudad) AS Rentas'+	 
                        ' FROM DIRECCION DP WHERE (DP.Pais=\'United States\' or DP.Pais=\'Estados Unidos\') and'+
						' (SELECT COUNT(*)'+
						' FROM RENTA RENTA1'+
						' INNER JOIN CLIENTE CLIENTE1 ON RENTA1.Cliente = CLIENTE1.Correo'+
						' INNER JOIN PELICULA PELICULA1 ON RENTA1.Pelicula = PELICULA1.Nombre'+
						' INNER JOIN DIRECCION DIRECCION1 ON CLIENTE1.idDireccion = DIRECCION1.idDireccion'+
						' WHERE (DIRECCION1.Pais=\'United States\' or DIRECCION1.Pais=\'Estados Unidos\') and'+
						' DIRECCION1.Ciudad=DP.Ciudad) >'+ 
						' (SELECT COUNT(*)'+
						' FROM RENTA RENTA2'+
						' INNER JOIN CLIENTE CLIENTE2 ON RENTA2.Cliente = CLIENTE2.Correo'+
						' INNER JOIN PELICULA PELICULA2 ON RENTA2.Pelicula = PELICULA2.Nombre'+
						' INNER JOIN DIRECCION DIRECCION2 ON CLIENTE2.idDireccion = DIRECCION2.idDireccion'+
						' WHERE DIRECCION2.Ciudad=\'Dayton\')'+
					    ' ORDER BY DP.Ciudad ASC;')
        cadena="<TABLE BORDER><TR><TH>No.</TH><TH>Ciudad</TH> <TH>Rentas</TH></TR>"
        rows = cur.fetchall()
        for row in range(len(rows)):
            cadena+="<TR><TD>"+str(row+1)
            cadena+="</TD><TD>"+str(rows[row][0])
            cadena+="</TD><TD>"+str(rows[row][1])
            cadena+="</TD></TR>"
        cadena+="</TABLE>"
        return cadena

    @app.route("/consulta10")
    def consulta10():    
        cur.execute('DROP TABLE IF EXISTS CONT_CAT;'+
                ' CREATE TEMP TABLE IF NOT EXISTS CONT_CAT AS'+ 				 
                ' SELECT DISTINCT DIRECCION.Ciudad, DIRECCION.Pais, CATEGORIA.Nombre, COUNT(*) AS CONT'+
                ' FROM RENTA'+
                ' INNER JOIN CLIENTE ON RENTA.Cliente = CLIENTE.Correo'+
                ' INNER JOIN PELICULA ON RENTA.Pelicula = PELICULA.Nombre'+
                ' INNER JOIN CATEGORIA ON RENTA.Pelicula = CATEGORIA.Pelicula'+
                ' INNER JOIN DIRECCION ON CLIENTE.idDireccion = DIRECCION.idDireccion'+ 
                ' GROUP BY DIRECCION.Ciudad, DIRECCION.Pais, CATEGORIA.Nombre'+
                ' ORDER BY Direccion.Pais ASC;'+
                ' SELECT CF.Ciudad, CF.Pais FROM CONT_CAT CF'+
                ' WHERE CF.CONT=(SELECT MAX (CONT) FROM CONT_CAT CC WHERE CC.Ciudad=CF.Ciudad and CC.Pais=CF.Pais)'+
                ' and CF.Nombre=\'Horror\';')
        cadena="<TABLE BORDER><TR><TH>No.</TH><TH>Ciudad</TH> <TH>Pais</TH></TR>"
        rows = cur.fetchall()
        for row in range(len(rows)):
            cadena+="<TR><TD>"+str(row+1)
            cadena+="</TD><TD>"+str(rows[row][0])
            cadena+="</TD><TD>"+str(rows[row][1])
            cadena+="</TD></TR>"
        cadena+="</TABLE>"
        return cadena

    @app.route("/eliminarTemporal")
    def eliminarTemporal():    
        cur.execute('DROP TABLE IF EXISTS TEMPORAL;')
        return "<h1>Tabla Temporal eliminada</h1>"
    
    @app.route("/eliminarModelo")
    def eliminarModelo():    
        cur.execute('DROP TABLE IF EXISTS RENTA;'+
                ' DROP TABLE IF EXISTS CATEGORIA;'+
                ' DROP TABLE IF EXISTS ACTOR;'+
                ' DROP TABLE IF EXISTS PELICULA;'+
                ' DROP TABLE IF EXISTS TIENDA;'+
                ' DROP TABLE IF EXISTS EMPLEADO;'+
                ' DROP TABLE IF EXISTS CLIENTE;'+
                ' DROP TABLE IF EXISTS DIRECCION;')
        return "<h1>Modelo Eliminado</h1>"

    @app.route("/cargarTemporal")
    def cargarTemporal():    
        relative=os.getcwd()
        #se crea la tabla temporal y se carga el csv
        with open(str(relative)+"/../[MIA]ScriptTT_201909103.sql","r") as archivo:
            paraejecutar=""
            for linea in archivo:
                paraejecutar+=linea
            cur.execute(paraejecutar)
        return "<h1>Se cargaron los datos a tabla temporal</h1>"

    @app.route("/cargarModelo")
    def cargarModelo():    
        relative=os.getcwd()
        #con este se crean las tablas
        with open(str(relative)+"/../[MIA]ScriptMR_201909103.sql","r") as archivo:
            paraejecutar=""
            for linea in archivo:
                paraejecutar+=linea
            cur.execute(paraejecutar)
        #con este se cargan los datos de la temporal al modelo
        with open(str(relative)+"/../[MIA]CargaDeDatos_201909103.sql","r") as archivo:
            paraejecutar=""
            for linea in archivo:
                paraejecutar+=linea  
            cur.execute(paraejecutar)
        return "<h1>Se cargaron los datos al modelo</h1>"

except:
    print("Error de base de datos")

