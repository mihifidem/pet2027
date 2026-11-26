from django.shortcuts import render

from .models import Servicio


def servicio_lista(request):
    servicios = Servicio.objects.filter(publicado=True)
    return render(request, "petadvisor/servicio_lista.html", {"servicios": servicios})

# Create your views here.
from django.shortcuts import get_object_or_404, render

def servicio_detalle(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk, publicado=True)
    valoraciones = servicio.valoraciones.all()
    return render(
        request,
        "petadvisor/servicio_detalle.html",
        {"servicio": servicio, "valoraciones": valoraciones},
    )