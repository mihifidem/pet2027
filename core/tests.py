from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from core.models import Autor, Editorial, Libro


class LibrosViewTests(TestCase):
    def test_listado_incluye_enlace_al_detalle(self):
        editorial = Editorial.objects.create(nombre="Editorial de prueba")
        libro = Libro.objects.create(
            titulo="Libro de prueba",
            nomberAutor="Autor de prueba",
            anio_publicacion=2026,
            editorial=editorial,
        )

        respuesta = self.client.get(reverse("core:libros"))

        self.assertContains(
            respuesta,
            f'href="{reverse("core:detalle_libro", kwargs={"id": libro.pk})}"',
        )


class SeedLibrosTests(TestCase):
    def test_seed_creates_related_data_and_can_be_repeated(self):
        editorial_existente = Editorial.objects.create(nombre="Editorial existente")
        libro_existente = Libro.objects.create(
            titulo="Libro existente",
            nomberAutor="Autor existente",
            anio_publicacion=2000,
            editorial=editorial_existente,
        )
        autor_existente = Autor.objects.create(
            nombre="Autor existente", email="existente@example.com"
        )
        autor_existente.libros.add(libro_existente)

        call_command("seed_libros", stdout=StringIO())

        self.assertEqual(Editorial.objects.count(), 4)
        self.assertEqual(Libro.objects.count(), 11)
        self.assertEqual(Autor.objects.count(), 6)
        for autor in Autor.objects.exclude(pk=autor_existente.pk):
            libros = list(autor.libros.all())
            self.assertEqual(len(libros), 2)
            self.assertEqual(len({libro.nomberAutor for libro in libros}), 1)
            self.assertEqual(autor.nombre, libros[0].nomberAutor)
            autor.full_clean()
        self.assertEqual(
            Autor.objects.get(nombre="Clara Montes").email,
            "clara.montes@example.com",
        )

        salida = StringIO()
        call_command("seed_libros", stdout=salida)

        self.assertEqual(Editorial.objects.count(), 4)
        self.assertEqual(Libro.objects.count(), 11)
        self.assertEqual(Autor.objects.count(), 6)
        self.assertEqual(list(autor_existente.libros.all()), [libro_existente])
        self.assertIn("0 editoriales, 0 libros y 0 autores", salida.getvalue())

    def test_reuses_matching_existing_books_and_editorial(self):
        editorial = Editorial.objects.create(nombre="Editorial Horizonte")
        libro = Libro.objects.create(
            titulo="El jardin de las estrellas",
            nomberAutor="Clara Montes",
            anio_publicacion=2018,
            editorial=editorial,
        )

        call_command("seed_libros", stdout=StringIO())

        self.assertEqual(Editorial.objects.count(), 3)
        self.assertEqual(Libro.objects.count(), 10)
        self.assertTrue(Autor.objects.filter(libros=libro).exists())

    def test_seed_fills_missing_email_without_overwriting_existing_email(self):
        clara = Autor.objects.create(nombre="Clara Montes", email="")
        daniel = Autor.objects.create(
            nombre="Daniel Robles", email="otro@example.com"
        )

        call_command("seed_libros", stdout=StringIO())

        clara.refresh_from_db()
        daniel.refresh_from_db()
        self.assertEqual(clara.email, "clara.montes@example.com")
        self.assertEqual(daniel.email, "otro@example.com")
        self.assertEqual(Autor.objects.count(), 5)
        self.assertEqual(clara.libros.count(), 2)
        self.assertEqual(daniel.libros.count(), 2)
