from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class CategoriaServicio(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="servicios",
    )
    categoria = models.ForeignKey(
        CategoriaServicio,
        on_delete=models.PROTECT,
        related_name="servicios",
    )
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    municipio = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    contacto_publico = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, blank=True)
    publicado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre
    
    
class ValoracionServicio(models.Model):
    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.CASCADE,
        related_name="valoraciones",
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="valoraciones",
    )
    puntuacion = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comentario = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["servicio", "autor"],
                name="valoracion_unica_por_autor_y_servicio",
            )
        ]

    def __str__(self):
        return f"{self.autor} → {self.servicio} ({self.puntuacion}/5)"


class FavoritoServicio(models.Model):
    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.CASCADE,
        related_name="favoritos",
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favoritos",
    )
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["servicio", "usuario"],
                name="favorito_unico_por_usuario_y_servicio",
            )
        ]

    def __str__(self):
        return f"{self.usuario} → {self.servicio}"
