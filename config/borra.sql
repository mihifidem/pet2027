create table libro(
    id integer primary key,
    titulo varchar(255),
    autor varchar(255),
    anio_publicacion integer
);
libro

id      titulo      autor      anio_publicacion
2       "Cien Años de Soledad" "Gabriel García Márquez" 1967
3       "La Sombra del Viento" "Carlos Ruiz Zafón" 2001
4       "Don Quijote de la Mancha" "Miguel de Cervantes" 1605
5       "El Principito" "Antoine de Saint-Exupéry" 1943
insert into libro (id, titulo, autor, anio_publicacion) values
(4, "Don Quijote de la Mancha", "Miguel de Cervantes", 1605),
(5, "El Principito", "Antoine de Saint-Exupéry", 1943);
insert into libro (id, titulo, autor, anio_publicacion) values
(1, "El Quijote", "Cervantes", 1605),
(2, "Cien Años de Soledad", "Gabriel García Márquez", 1967),
(3, "La Sombra del Viento", "Carlos Ruiz Zafón", 2001);

select * from libro;
#list libros
select * from libro where anio_publicacion > 2000;
select * from libro where autor like "%Cervantes%";
select * from libro where titulo like "%Quijote%";
select * from libro where anio_publicacion < 1900;
select * from libro where autor like "%Gabriel García Márquez%";
select * from libro where titulo like "%El Principito%";
select * from libro where id = 1;

update libro set titulo = "El Quijote Modificado" where id = 1;
delete from libro where id = 1;

