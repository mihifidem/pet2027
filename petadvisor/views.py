from django.shortcuts import render

from .models import Servicio


def servicio_lista(request):
    servicios = Servicio.objects.filter(publicado=True)
    return render(request, "petadvisor/servicio_lista.html", {"servicios": servicios})

# Create your views here.
