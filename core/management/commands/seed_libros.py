from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import Autor, Editorial, Libro


DATOS = [
    (
        "Editorial Horizonte",
        "Clara Montes",
        "clara.montes@example.com",
        [("El jardin de las estrellas", 2018), ("Cartas al viento", 2021)],
    ),
    (
        "Editorial Horizonte",
        "Daniel Robles",
        "daniel.robles@example.com",
        [("La ciudad sumergida", 2019), ("El mapa de los suenos", 2023)],
    ),
    (
        "Ediciones Brisa",
        "Lucia del Valle",
        "lucia.delvalle@example.com",
        [("La casa de los relojes", 2017), ("Una noche de invierno", 2022)],
    ),
    (
        "Ediciones Brisa",
        "Mateo Soler",
        "mateo.soler@example.com",
        [("Viaje al bosque azul", 2020), ("Las puertas del mar", 2024)],
    ),
    (
        "Libros del Faro",
        "Sofia Rivas",
        "sofia.rivas@example.com",
        [("El secreto de la montana", 2016), ("Los dias de papel", 2025)],
    ),
]


class Command(BaseCommand):
    help = "Carga libros, editoriales y autores ficticios sin borrar datos existentes."

    @transaction.atomic
    def handle(self, *args, **options):
        editoriales_creadas = 0
        libros_creados = 0
        autores_creados = 0

        for editorial_nombre, autor_nombre, autor_email, titulos in DATOS:
            editorial = Editorial.objects.filter(nombre=editorial_nombre).first()
            if editorial is None:
                editorial = Editorial.objects.create(nombre=editorial_nombre)
                editoriales_creadas += 1

            libros = []
            for titulo, anio in titulos:
                datos_libro = {
                    "titulo": titulo,
                    "nomberAutor": autor_nombre,
                    "anio_publicacion": anio,
                    "editorial": editorial,
                }
                libro = Libro.objects.filter(**datos_libro).first()
                if libro is None:
                    libro = Libro.objects.create(**datos_libro)
                    libros_creados += 1
                libros.append(libro)

            autor = Autor.objects.filter(nombre=autor_nombre).first()
            if autor is None:
                autor = Autor.objects.create(nombre=autor_nombre, email=autor_email)
                autores_creados += 1
            elif not autor.email:
                autor.email = autor_email
                autor.save(update_fields=["email"])
            autor.libros.add(*libros)

        self.stdout.write(
            self.style.SUCCESS(
                f"Datos creados: {editoriales_creadas} editoriales, "
                f"{libros_creados} libros y {autores_creados} autores."
            )
        )
