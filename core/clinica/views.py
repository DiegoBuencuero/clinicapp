from django.shortcuts import render
from .models import Clinica
# Create your views here.
def dashboard(request):
    return render (request, "dashboard.html")


def inicio(request):
    clinicas = Clinica.objects.all()
    return render (request, "landing.html", {"clinicas": clinicas})

def clinica_detalle(request, id):
    try:
        clinica = Clinica.objects.get(id=id)
        return render(request, 'clinica_detalle.html', {'clinica': clinica})
    except Clinica.DoesNotExist:
        return render(request, 'pag_error.html')  