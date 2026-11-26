import email

from django.db import models

class Editorial(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    titulo = models.CharField(max_length=255)
    nomberAutor = models.CharField(max_length=255)
    anio_publicacion = models.IntegerField()
    editorial = models.ForeignKey('Editorial', on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

class Autor(models.Model):
    libros = models.ManyToManyField('Libro')
    nombre = models.CharField(max_length=255)
    email = models.EmailField()
    
    def __str__(self):
        return self.nombre

class fileLibro(models.Model):
    libro = models.OneToOneField('Libro', on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='libros/')

    def __str__(self):
        return self.archivo.name