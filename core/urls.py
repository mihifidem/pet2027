#rutas
from django.urls import path, include
from . import views
app_name = 'core'
urlpatterns = [
    #ruta principal
    path('home/', views.home, name='home'), 
    path('libros/', views.libros, name='libros'),
    path('libro/<int:id>/', views.libro, name='detalle_libro'),
    path('autores/', views.autores, name='autores'),
    path('autor/<int:id>/', views.autor, name='detalle_autor'),

]

# Nota: Asegúrate de que en tus plantillas uses {% url 'core:detalle_libro' id=libro.pk %} para generar los enlaces correctamente.