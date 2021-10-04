-- William Alejandro Borrayo Alarcón - 201909103
-- Database: practica

DROP TABLE IF EXISTS RENTA;
DROP TABLE IF EXISTS CATEGORIA;
DROP TABLE IF EXISTS ACTOR;
DROP TABLE IF EXISTS PELICULA;
DROP TABLE IF EXISTS TIENDA;
DROP TABLE IF EXISTS EMPLEADO;
DROP TABLE IF EXISTS CLIENTE;
DROP TABLE IF EXISTS DIRECCION;

------------------------------------------------------------------------- TABLA DIRECCION
CREATE TABLE IF NOT EXISTS PUBLIC.DIRECCION(
	idDireccion SERIAL PRIMARY KEY,
	Domicilio VARCHAR,  -- Para lo que dice direccion
	CodigoPostal VARCHAR,
	Ciudad VARCHAR,
	Pais VARCHAR
);
				 
------------------------------------------------------------------------- TABLA CLIENTE
CREATE TABLE IF NOT EXISTS PUBLIC.CLIENTE(
	Nombre VARCHAR, 
	Apellido VARCHAR,
	Correo VARCHAR PRIMARY KEY,
	Activo VARCHAR,
	FechaRegistro VARCHAR,
	TiendaPreferida VARCHAR,
	idDireccion INTEGER,
	Rentas INTEGER,
	FOREIGN KEY (idDireccion)
	REFERENCES DIRECCION(idDireccion)
);

------------------------------------------------------------------------- TABLA EMPLEADO
CREATE TABLE IF NOT EXISTS PUBLIC.EMPLEADO(
	Nombre VARCHAR, 
	Apellido VARCHAR,
	Correo VARCHAR PRIMARY KEY,
	Activo VARCHAR,
	TiendaAsignada VARCHAR,
	Usuario VARCHAR,
	Contrasenia VARCHAR,
	idDireccion INTEGER,
	FOREIGN KEY (idDireccion)
	REFERENCES DIRECCION(idDireccion)
);

------------------------------------------------------------------------- TABLA TIENDA
CREATE TABLE IF NOT EXISTS PUBLIC.TIENDA(
	Nombre VARCHAR PRIMARY KEY, 
	EncargadoNombre VARCHAR,
	EncargadoApellido VARCHAR,
	idDireccion INTEGER,
	FOREIGN KEY (idDireccion)
	REFERENCES DIRECCION(idDireccion)
);

------------------------------------------------------------------------- TABLA PELICULA
CREATE TABLE IF NOT EXISTS PUBLIC.PELICULA(
	Tienda VARCHAR,
	Nombre VARCHAR PRIMARY KEY,
	Descripcion VARCHAR,
	AnioLanzamiento VARCHAR,
	DiasRenta VARCHAR,
	CostoRenta VARCHAR,
	Duracion VARCHAR,
	CostoDanio VARCHAR,
	Clasificacion VARCHAR,
	Lenguaje VARCHAR,
	Cantidad INTEGER,
	FOREIGN KEY(Tienda)
	REFERENCES TIENDA(Nombre)
);
				 
------------------------------------------------------------------------- TABLA ACTOR
CREATE TABLE IF NOT EXISTS PUBLIC.ACTOR(
	NombreCompleto VARCHAR,
	Nombre VARCHAR,
	Apellido VARCHAR,
	Pelicula VARCHAR,
	PRIMARY KEY (NombreCompleto, Pelicula),
	FOREIGN KEY (Pelicula) REFERENCES PELICULA(Nombre)
);

------------------------------------------------------------------------- TABLA CATEGORIA
CREATE TABLE IF NOT EXISTS PUBLIC.CATEGORIA(
	Nombre VARCHAR,
	Pelicula VARCHAR,
	PRIMARY KEY (Nombre, Pelicula),
	FOREIGN KEY (Pelicula) REFERENCES PELICULA(Nombre)
);
				 
------------------------------------------------------------------------- TABLA RENTA
CREATE TABLE IF NOT EXISTS PUBLIC.RENTA(
	idRenta SERIAL PRIMARY KEY,
	FechaRenta VARCHAR,
	FechaRetorno VARCHAR,
	MontoPagar DECIMAL,
	FechaPago VARCHAR,
	Cliente VARCHAR,
	Tienda VARCHAR,
	Pelicula VARCHAR,
	FOREIGN KEY (Cliente) REFERENCES CLIENTE(Correo),
	FOREIGN KEY (Tienda) REFERENCES TIENDA(Nombre),
	FOREIGN KEY (Pelicula) REFERENCES PELICULA(Nombre)
);
