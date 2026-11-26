

# Register your models here.
from django.contrib import admin

from .models import (
    CategoriaServicio, 
    Servicio,
    FavoritoServicio,
    ValoracionServicio,
)
    

admin.site.register(CategoriaServicio)
admin.site.register(Servicio)
admin.site.register(ValoracionServicio)
admin.site.register(FavoritoServicio)