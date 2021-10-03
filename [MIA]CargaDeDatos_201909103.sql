-- William Alejandro Borrayo Alarcón - 201909103

------------------------------------------------------------------------- TABLA DIRECCION

-- Se insertan las direcciones de clientes
INSERT INTO DIRECCION (Domicilio, CodigoPostal, Ciudad, Pais)
SELECT DISTINCT DIRECCION_CLIENTE, CODIGO_POSTAL_CLIENTE, CIUDAD_CLIENTE, PAIS_CLIENTE from TEMPORAL
WHERE NOT EXISTS(SELECT FROM DIRECCION WHERE 
				 Domicilio=DIRECCION_CLIENTE and
				 CodigoPostal=CODIGO_POSTAL_CLIENTE and
				 Ciudad=CIUDAD_CLIENTE and
				 Pais=PAIS_CLIENTE) and
				 not(DIRECCION_CLIENTE='-' and CODIGO_POSTAL_CLIENTE='-' and CIUDAD_CLIENTE='-' and PAIS_CLIENTE='-') and
				 not(NOMBRE_CLIENTE='-') and
				 not(NOMBRE_TIENDA='-') and
				 not(NOMBRE_EMPLEADO='-') and 
				 not(CODIGO_POSTAL_CLIENTE='-');

-- Se insertan las direcciones de Empleados
INSERT INTO DIRECCION (Domicilio, CodigoPostal, Ciudad, Pais)
SELECT DISTINCT DIRECCION_EMPLEADO, CODIGO_POSTAL_EMPLEADO, CIUDAD_EMPLEADO, PAIS_EMPLEADO FROM TEMPORAL
WHERE NOT EXISTS(SELECT FROM DIRECCION WHERE 
				 Domicilio=DIRECCION_EMPLEADO and
				 CodigoPostal=CODIGO_POSTAL_EMPLEADO and
				 Ciudad=CIUDAD_EMPLEADO and
				 Pais=PAIS_EMPLEADO) and
				 not(DIRECCION_EMPLEADO='-' and CODIGO_POSTAL_EMPLEADO='-' and CIUDAD_EMPLEADO='-' and PAIS_EMPLEADO='-') and
				 not(NOMBRE_CLIENTE='-') and
				 not(NOMBRE_TIENDA='-') and
				 not(NOMBRE_EMPLEADO='-');
				 
-- Se insertan las direcciones de Tiendas
INSERT INTO DIRECCION (Domicilio, CodigoPostal, Ciudad, Pais)
SELECT DISTINCT DIRECCION_TIENDA, CODIGO_POSTAL_TIENDA, CIUDAD_TIENDA, PAIS_TIENDA FROM TEMPORAL
WHERE NOT EXISTS(SELECT FROM DIRECCION WHERE 
				 Domicilio=DIRECCION_TIENDA and
				 CodigoPostal=CODIGO_POSTAL_TIENDA and
				 Ciudad=CIUDAD_TIENDA and
				 Pais=PAIS_TIENDA) and
				 not(DIRECCION_TIENDA='-' and CODIGO_POSTAL_TIENDA='-' and CIUDAD_TIENDA='-' and PAIS_TIENDA='-') and
				 not(NOMBRE_CLIENTE='-') and
				 not(NOMBRE_TIENDA='-') and
				 not(NOMBRE_EMPLEADO='-');
				 
------------------------------------------------------------------------- TABLA CLIENTE
INSERT INTO CLIENTE
  SELECT 
  split_part(NOMBRE_CLIENTE, ' ', 1),
  split_part(NOMBRE_CLIENTE, ' ', 2),
  CORREO_CLIENTE,
  CLIENTE_ACTIVO,
  FECHA_CREACION,
  TIENDA_PREFERIDA,
  (SELECT idDireccion FROM DIRECCION WHERE Domicilio=DIRECCION_CLIENTE)
  FROM TEMPORAL
   WHERE not (
	   NOMBRE_CLIENTE='-' and 
	   CORREO_CLIENTE='-' and 
	   CLIENTE_ACTIVO='-' and 
	   FECHA_CREACION='-' and
	   TIENDA_PREFERIDA='_') and not (CORREO_CLIENTE='-')
	   and not(CODIGO_POSTAL_CLIENTE='-')
	   and EXISTS(SELECT idDireccion FROM DIRECCION WHERE Domicilio=DIRECCION_CLIENTE)
   ON CONFLICT (Correo)
DO NOTHING;

------------------------------------------------------------------------- TABLA EMPLEADO
INSERT INTO EMPLEADO
  SELECT 
  split_part(NOMBRE_EMPLEADO, ' ', 1),
  split_part(NOMBRE_EMPLEADO, ' ', 2),
  CORREO_EMPLEADO,
  EMPLEADO_ACTIVO,
  TIENDA_EMPLEADO,
  USUARIO_EMPLEADO,
  CONTRASENIA_EMPLEADO,
  (SELECT idDireccion FROM DIRECCION WHERE Domicilio=DIRECCION_CLIENTE)
  FROM TEMPORAL
   WHERE not (
	   NOMBRE_EMPLEADO='-' and 
	   CORREO_EMPLEADO='-' and 
	   EMPLEADO_ACTIVO='-' and 
	   TIENDA_EMPLEADO='-' and
	   USUARIO_EMPLEADO='_' and
	   CONTRASENIA_EMPLEADO='_' and
   	   DIRECCION_EMPLEADO='-' and 
	   CODIGO_POSTAL_EMPLEADO='-' and 
	   CIUDAD_EMPLEADO='-' and 
	   PAIS_EMPLEADO='-') and not (CORREO_EMPLEADO='-')
	   and EXISTS(SELECT idDireccion FROM DIRECCION WHERE Domicilio=DIRECCION_EMPLEADO)
   ON CONFLICT (Correo)
DO NOTHING;

------------------------------------------------------------------------- TABLA TIENDA
INSERT INTO TIENDA
  SELECT 
  NOMBRE_TIENDA,
  split_part(ENCARGADO_TIENDA, ' ', 1),
  split_part(ENCARGADO_TIENDA, ' ', 2),
  (SELECT idDireccion FROM DIRECCION WHERE Domicilio=DIRECCION_CLIENTE)
  FROM TEMPORAL
   WHERE not (
	   NOMBRE_TIENDA='-' and 
	   ENCARGADO_TIENDA='-' and 
	   EMPLEADO_ACTIVO='-' and 
	   TIENDA_EMPLEADO='-' and
	   USUARIO_EMPLEADO='_' and
	   CONTRASENIA_EMPLEADO='_' and
   	   DIRECCION_EMPLEADO='-') 
		  and not (NOMBRE_TIENDA='-')
	   and EXISTS(SELECT idDireccion FROM DIRECCION WHERE Domicilio=DIRECCION_TIENDA)
   ON CONFLICT (Nombre)
DO NOTHING;

------------------------------------------------------------------------- TABLA PELICULA
INSERT INTO PELICULA
SELECT 
TIENDA_PELICULA,
NOMBRE_PELICULA,
DESCRIPCION_PELICULA,
ANIO_LANZAMIENTO,
DIAS_RENTA,
COSTO_RENTA,
DURACION,
COSTO_POR_DANIO,
CLASIFICACION,
LENGUAJE_PELICULA,
CATEGORIA_PELICULA
FROM TEMPORAL
WHERE not (TIENDA_PELICULA='-')
	  and not (NOMBRE_PELICULA='-')
	  and EXISTS (SELECT Nombre FROM TIENDA WHERE Nombre=TIENDA_PELICULA)
ON CONFLICT(Nombre)
DO NOTHING;
				 
------------------------------------------------------------------------- TABLA ACTOR
INSERT INTO ACTOR
SELECT DISTINCT
  ACTOR_PELICULA,
  split_part(ACTOR_PELICULA, ' ', 1),
  split_part(ACTOR_PELICULA, ' ', 2),
  NOMBRE_PELICULA
FROM TEMPORAL
WHERE NOT(ACTOR_PELICULA='-' and NOMBRE_PELICULA='-') and not (ACTOR_PELICULA='-')
	and EXISTS(SELECT Nombre FROM PELICULA WHERE Nombre=NOMBRE_PELICULA) -- HACER ESTO CON LAS LLAVES FORANEAS
   ON CONFLICT (NombreCompleto, Pelicula)
DO NOTHING;
				 
------------------------------------------------------------------------- TABLA RENTA
INSERT INTO RENTA (FechaRenta, FechaRetorno, MontoPagar, FechaPago, Cliente, Tienda, Pelicula)
SELECT DISTINCT
  FECHA_RENTA,
  FECHA_RETORNO,
  MONTO_A_PAGAR::DECIMAL,
  FECHA_PAGO,
  CORREO_CLIENTE,
  NOMBRE_TIENDA,
  NOMBRE_PELICULA
FROM TEMPORAL
WHERE NOT EXISTS (SELECT FROM RENTA WHERE FechaRenta=FECHA_RENTA and
				 FechaRetorno=FECHA_RETORNO and MontoPagar=MONTO_A_PAGAR::DECIMAL and
				 FechaPago=FECHA_PAGO and Cliente=CORREO_CLIENTE and
				 Tienda=NOMBRE_TIENDA and Pelicula=NOMBRE_PELICULA)
				 and not (FECHA_RENTA='-')
				 and not (NOMBRE_CLIENTE='-')
				 and not (FECHA_RETORNO='-')
				 and EXISTS (SELECT Correo FROM CLIENTE WHERE Correo=CORREO_CLIENTE)
				 and EXISTS (SELECT Nombre FROM TIENDA WHERE Nombre=NOMBRE_TIENDA)
				 and EXISTS (SELECT Nombre FROM PELICULA WHERE Nombre=NOMBRE_PELICULA);

-- Se actualizan las rentas para cada cliente
UPDATE CLIENTE CF SET Rentas=(SELECT COUNT(*) FROM RENTA INNER JOIN CLIENTE CL ON RENTA.Cliente=CL.Correo 
WHERE CL.Nombre=CF.Nombre and CL.Apellido=CF.Apellido and CL.Correo=CF.Correo);

-- Para actualizar la cantidad de cada pelicula
UPDATE PELICULA SET Cantidad=(SELECT COUNT(*) FROM
(SELECT DISTINCT Pelicula, FechaRenta, Cliente FROM RENTA WHERE Pelicula=Nombre) AS FOO);
				
