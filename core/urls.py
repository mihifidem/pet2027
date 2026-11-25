#rutas
from django.urls import path, include
from . import views
urlpatterns = [
    #ruta principal
    path('home/', views.home, name='home'), 
]