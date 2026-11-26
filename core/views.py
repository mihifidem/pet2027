from urllib import response

from django.shortcuts import render
from django.http import HttpResponse

from core.models import Libro, Autor

# Create your views here.
def home(request):
    return render(request, 'core/home_app.html')

def libros(request):
    libros = Libro.objects.all()
    context = {
        'libros': libros
    }
    return render(request, 'core/libros_app.html', context)

def libro(request, id):
    libro = Libro.objects.get(id=id)
    context = {
        'libro': libro
    }
    return render(request, 'core/libro_app.html', context)

def autores(request):
    autores = Autor.objects.all()
    context = {
        'autores': autores
    }
    return render(request, 'core/autores_app.html', context)

def autor(request, id):
    autor = Autor.objects.get(id=id)
    libros_autor = autor.libros.all()
    context = {
        'autor': autor,
        'libros_autor': libros_autor
    }
    return render(request, 'core/autor_app.html', context)