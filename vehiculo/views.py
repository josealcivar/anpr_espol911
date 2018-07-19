from django.shortcuts import render, redirect
from django.views.generic import ListView
from vehiculo.models import Vehiculo

# Create your views here.

def index(request):
    return render(request, 'index.html')

def consults(request):
    return render(request, 'vehiculo/consult.html')


class VehiculoList(ListView):
    model         = Vehiculo
    template_name = 'vehiculo/consult.html'
    # paginate_by = 10
