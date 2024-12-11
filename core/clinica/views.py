from django.shortcuts import render
from .models import Clinica
# Create your views here.
def dashboard(request):
    return render (request, "dashboard.html")


def inicio(request):
    clinicas = Clinica.objects.all()
    return render (request, "landing.html", {"clinicas": clinicas})
