import psycopg2

from flask import Flask, json, request
from flask_restful import Resource, Api, reqparse
from flask_jsonpify import jsonify, jsonpify
from flask_cors import CORS, cross_origin
import sys

app = Flask(__name__)

CORS(app)

connection = "host=%s port=%s user=%s password=%s dbname=%s" % ('localhost', 5432, 'william', 201909103, 'practica')

try:
    conn = psycopg2.connect(connection)
    cur = conn.cursor()

    @app.route("/")
    def home_view():
        return "<h1>Hello World8!</h1>"

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
        cur.execute('SELECT NombreCompleto FROM ACTOR WHERE (position(\'son\' in LOWER(Apellido))>0) ORDER BY Nombre ASC;')
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
        cur.execute('SELECT DIRECCION.Pais, CLIENTE.Nombre, CLIENTE.Apellido,'+
					 ' CONCAT(ROUND(((CLIENTE.Rentas)::DECIMAL*100 /'+
                    ' (SELECT SUM(Rentas) FROM CLIENTE)::DECIMAL)::DECIMAL, 2),\' %\') as porcentaje '+
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
        for row in range(len(rows)):
            cadena+="<TR><TD>"+str(row+1)
            cadena+="</TD><TD>"+str(rows[row][0])
            cadena+="</TD><TD>"+str(rows[row][1])
            cadena+="</TD><TD>"+str(rows[row][2])
            cadena+="</TD><TD>"+str(rows[row][3])
            cadena+="</TD></TR>"
        cadena+="</TABLE>"
        return cadena

except:
    print("Error de base de datos")

