from django.conf import settings
from django.db import models


class Protectora(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    localidad = models.CharField(max_length=120)
    provincia = models.CharField(max_length=120)
    contacto_publico = models.CharField(max_length=255)
    activa = models.BooleanField(default=True)
    creada_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.localidad})"


class MiembroProtectora(models.Model):

    class Rol(models.TextChoices):
        RESPONSABLE = "responsable", "Responsable"
        COLABORADOR = "colaborador", "Colaborador"

    protectora = models.ForeignKey(
        Protectora,
        on_delete=models.CASCADE,
        related_name="miembros"
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pertenencias_protectora"
    )

    rol = models.CharField(
        max_length=20,
        choices=Rol.choices,
        default=Rol.COLABORADOR
    )

    fecha_alta = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["protectora", "usuario"],
                name="unique_usuario_por_protectora"
            )
        ]

    def __str__(self):
        return f"{self.usuario} - {self.protectora} ({self.get_rol_display()})"


class Animal(models.Model):

    class Especie(models.TextChoices):
        PERRO = "perro", "Perro"
        GATO = "gato", "Gato"
        OTRO = "otro", "Otro"

    class Sexo(models.TextChoices):
        MACHO = "macho", "Macho"
        HEMBRA = "hembra", "Hembra"
        DESCONOCIDO = "desconocido", "Desconocido"

    class Tamano(models.TextChoices):
        PEQUENO = "pequeno", "Pequeño"
        MEDIANO = "mediano", "Mediano"
        GRANDE = "grande", "Grande"

    class Compatibilidad(models.TextChoices):
        SIN_EVALUAR = "sin_evaluar", "Sin evaluar"
        APTO = "apto", "Apto"
        CON_PRECAUCION = "con_precaucion", "Con precaución"
        NO_APTO = "no_apto", "No apto"

    class EstadoPublicacion(models.TextChoices):
        BORRADOR = "borrador", "Borrador"
        PUBLICADO = "publicado", "Publicado"
        ARCHIVADO = "archivado", "Archivado"

    class EstadoDisponibilidad(models.TextChoices):
        DISPONIBLE = "disponible", "Disponible"
        RESERVADO = "reservado", "Reservado"
        ADOPTADO = "adoptado", "Adoptado"
        NO_DISPONIBLE = "no_disponible", "Temporalmente no disponible"

    protectora = models.ForeignKey(
        Protectora,
        on_delete=models.CASCADE,
        related_name="animales"
    )

    nombre = models.CharField(max_length=120)

    especie = models.CharField(
        max_length=20,
        choices=Especie.choices
    )

    raza = models.CharField(
        max_length=120,
        blank=True
    )

    sexo = models.CharField(
        max_length=20,
        choices=Sexo.choices,
        default=Sexo.DESCONOCIDO
    )

    fecha_nacimiento_estimada = models.DateField(
        blank=True,
        null=True
    )

    tamano = models.CharField(
        max_length=20,
        choices=Tamano.choices
    )

    descripcion = models.TextField()

    compatibilidad_ninos = models.CharField(
        max_length=20,
        choices=Compatibilidad.choices,
        default=Compatibilidad.SIN_EVALUAR
    )

    compatibilidad_animales = models.CharField(
        max_length=20,
        choices=Compatibilidad.choices,
        default=Compatibilidad.SIN_EVALUAR
    )

    observaciones_comportamiento = models.TextField(blank=True)

    estado_publicacion = models.CharField(
        max_length=20,
        choices=EstadoPublicacion.choices,
        default=EstadoPublicacion.BORRADOR
    )

    estado_disponibilidad = models.CharField(
        max_length=20,
        choices=EstadoDisponibilidad.choices,
        default=EstadoDisponibilidad.DISPONIBLE
    )

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_especie_display()})"


class FotoAnimal(models.Model):

    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name="fotos"
    )

    imagen = models.ImageField(
        upload_to="animales/%Y/%m/"
    )

    texto_alternativo = models.CharField(max_length=200)

    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden", "id"]

    def __str__(self):
        return f"Foto {self.orden} - {self.animal.nombre}"