from django.urls import path

from . import views

app_name = "petadvisor"

urlpatterns = [
    path("", views.servicio_lista, name="servicio_lista"),
]