-- William Alejandro Borrayo Alarcón - 201909103

-- 1)
-- RESULTADO = 17	 
SELECT Nombre, Cantidad FROM PELICULA WHERE Nombre='SUGAR WONKA';
					 
-- 2)
-- RESULTADO = 6 CLIENTES
SELECT DISTINCT CLIENTE.Nombre, CLIENTE.Apellido, 
					 (SELECT SUM(CAST(RENTA1.MontoPagar AS DECIMAL)) FROM RENTA RENTA1 INNER JOIN CLIENTE CLIENTE1 
					  ON RENTA1.Cliente = CLIENTE1.Correo WHERE CLIENTE1.Correo=CLIENTE.Correo)as Monto 
FROM CLIENTE INNER JOIN RENTA ON CLIENTE.Correo = RENTA.Cliente 
WHERE CLIENTE.Rentas >39;					 
					
-- 3) 
SELECT DISTINCT NombreCompleto FROM ACTOR WHERE (position('son' in LOWER(Apellido))>0) ORDER BY NombreCompleto ASC;

-- 4)
SELECT PELICULA.Nombre, PELICULA.Descripcion, ACTOR.NombreCompleto, Pelicula.AnioLanzamiento
FROM PELICULA INNER JOIN ACTOR ON PELICULA.Nombre = ACTOR.Pelicula 
WHERE( (position('crocodile' in LOWER(PELICULA.Descripcion))>0) and 
	   (position('shark' in LOWER(PELICULA.Descripcion))>0) and
	 	not ACTOR.NombreCompleto='-') 
ORDER BY ACTOR.Apellido ASC;

-- 5)
SELECT DISTINCT DIRECCION.Pais, CLIENTE.Nombre, CLIENTE.Apellido,
					 CONCAT(ROUND(((CLIENTE.Rentas)::DECIMAL*100
								   /
					(SELECT SUM(Rentas) FROM CLIENTE CL  INNER JOIN DIRECCION DR
					 ON CL.idDireccion=DR.idDireccion
					 WHERE DR.Pais=DIRECCION.Pais)::DECIMAL)::DECIMAL, 2),' %') as porcentaje 
FROM DIRECCION INNER JOIN CLIENTE ON DIRECCION.idDireccion = CLIENTE.idDireccion 
WHERE CLIENTE.Rentas = (SELECT MAX (Rentas) FROM CLIENTE);
	 
-- 6)
SELECT DISTINCT (SELECT COUNT(*) FROM CLIENTE) AS TOTAL_CLIENTES, D.Pais, D.Ciudad, CONCAT(ROUND((
	SELECT COUNT(*)
	FROM DIRECCION INNER JOIN CLIENTE ON DIRECCION.idDireccion = CLIENTE.idDireccion
	WHERE DIRECCION.Pais=D.Pais AND DIRECCION.Ciudad=D.Ciudad
	GROUP BY DIRECCION.Pais, DIRECCION.Ciudad)::DECIMAL*100
					 /
	(SELECT COUNT(*)
	FROM DIRECCION INNER JOIN CLIENTE ON DIRECCION.idDireccion = CLIENTE.idDireccion
	WHERE DIRECCION.Pais=D.Pais
	GROUP BY DIRECCION.Pais)::DECIMAL, 2), ' %') as Porcentaje
FROM DIRECCION D ORDER BY D.Pais ASC;

-- 7)  
-- promedio = (rentas totales pais y ciudad)/(no.ciudades por pais) DEFINITIVE
SELECT DISTINCT DP.Pais, DP.Ciudad, (SELECT COUNT(*)
									FROM RENTA
									INNER JOIN CLIENTE ON RENTA.Cliente = CLIENTE.Correo
									INNER JOIN DIRECCION ON CLIENTE.idDireccion = DIRECCION.idDireccion
									WHERE DIRECCION.Pais=DP.Pais and DIRECCION.Ciudad=DP.Ciudad) AS Rentas,
	(
	ROUND((SELECT COUNT(*)
				FROM RENTA
				INNER JOIN CLIENTE ON RENTA.Cliente = CLIENTE.Correo
				INNER JOIN DIRECCION ON CLIENTE.idDireccion = DIRECCION.idDireccion
				WHERE DIRECCION.Pais=DP.Pais and DIRECCION.Ciudad=DP.Ciudad)::DECIMAL
							/
	(SELECT COUNT(*) FROM DIRECCION DCP WHERE DCP.Pais=DP.Pais GROUP BY DCP.Pais)::DECIMAL,2)
	)AS Promedio
FROM DIRECCION DP ORDER BY DP.Pais ASC, DP.Ciudad ASC;

--8)
--porcentaje de rentas=(rentas de sport por pais)*100 / (rentas por pais)
SELECT DISTINCT DP.Pais, CONCAT(ROUND((
	(SELECT COUNT(*)
		FROM RENTA RENTA2
		INNER JOIN CLIENTE CLIENTE2  ON RENTA2.Cliente = CLIENTE2.Correo
		INNER JOIN PELICULA PELICULA2 ON RENTA2.Pelicula = PELICULA2.Nombre
	 	INNER JOIN CATEGORIA CATEGORIA2 ON RENTA2.Pelicula = CATEGORIA2.Pelicula
		INNER JOIN DIRECCION DIRECCION2 ON CLIENTE2.idDireccion = DIRECCION2.idDireccion
		WHERE DIRECCION2.Pais=DP.Pais and CATEGORIA2.Nombre='Sports' HAVING COUNT(*)>0)::DECIMAL*100
		/
	NULLIF((SELECT DISTINCT COUNT(*)
		FROM RENTA RENTA1
		INNER JOIN CLIENTE CLIENTE1  ON RENTA1.Cliente = CLIENTE1.Correo
		INNER JOIN PELICULA PELICULA1 ON RENTA1.Pelicula = PELICULA1.Nombre
		INNER JOIN CATEGORIA CATEGORIA1 ON RENTA1.Pelicula = CATEGORIA1.Pelicula
		INNER JOIN DIRECCION DIRECCION1 ON CLIENTE1.idDireccion = DIRECCION1.idDireccion
		WHERE DIRECCION1.Pais=DP.Pais
	    HAVING COUNT(*)>0)::DECIMAL,0)
		),2), ' %') AS PORCENTAJE_SPORTS
FROM DIRECCION DP ORDER BY DP.Pais ASC;
					 				 
--9)
SELECT DISTINCT DP.Ciudad, (SELECT COUNT(*)
						FROM RENTA 
						INNER JOIN CLIENTE ON RENTA.Cliente = CLIENTE.Correo
						INNER JOIN PELICULA ON RENTA.Pelicula = PELICULA.Nombre
						INNER JOIN DIRECCION ON CLIENTE.idDireccion = DIRECCION.idDireccion
						WHERE (DIRECCION.Pais='United States' or DIRECCION.Pais='Estados Unidos') and
						 DIRECCION.Ciudad=DP.Ciudad) AS Rentas	 
FROM DIRECCION DP WHERE (DP.Pais='United States' or DP.Pais='Estados Unidos') and
					 -- rentas > rentas dayton
						(SELECT COUNT(*)
						FROM RENTA RENTA1 
						INNER JOIN CLIENTE CLIENTE1 ON RENTA1.Cliente = CLIENTE1.Correo
						INNER JOIN PELICULA PELICULA1 ON RENTA1.Pelicula = PELICULA1.Nombre
						INNER JOIN DIRECCION DIRECCION1 ON CLIENTE1.idDireccion = DIRECCION1.idDireccion
						WHERE (DIRECCION1.Pais='United States' or DIRECCION1.Pais='Estados Unidos') and
						 DIRECCION1.Ciudad=DP.Ciudad)
						 >
						(SELECT COUNT(*)
						FROM RENTA RENTA2
						INNER JOIN CLIENTE CLIENTE2 ON RENTA2.Cliente = CLIENTE2.Correo
						INNER JOIN PELICULA PELICULA2 ON RENTA2.Pelicula = PELICULA2.Nombre
						INNER JOIN DIRECCION DIRECCION2 ON CLIENTE2.idDireccion = DIRECCION2.idDireccion
						WHERE DIRECCION2.Ciudad='Dayton')
					 ORDER BY DP.Ciudad ASC;
					 
--10)
--CUIDADES POR PAIS EN RENTAS
DROP TABLE IF EXISTS CONT_CAT;
CREATE TEMP TABLE IF NOT EXISTS CONT_CAT AS 				 
	SELECT DIRECCION.Ciudad, DIRECCION.Pais, CATEGORIA.Nombre, COUNT(*) AS CONT
	FROM RENTA 
	INNER JOIN CLIENTE ON RENTA.Cliente = CLIENTE.Correo
	INNER JOIN PELICULA ON RENTA.Pelicula = PELICULA.Nombre
	INNER JOIN CATEGORIA ON RENTA.Pelicula = CATEGORIA.Pelicula
	INNER JOIN DIRECCION ON CLIENTE.idDireccion = DIRECCION.idDireccion 
	GROUP BY DIRECCION.Ciudad, DIRECCION.Pais, CATEGORIA.Nombre
	ORDER BY Direccion.Pais ASC;

SELECT CF.Ciudad, CF.Pais FROM CONT_CAT CF
 WHERE CF.CONT=(SELECT MAX (CONT) FROM CONT_CAT CC WHERE CC.Ciudad=CF.Ciudad and CC.Pais=CF.Pais)
 and CF.Nombre='Horror';
					 
