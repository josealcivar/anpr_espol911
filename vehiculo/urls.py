from django.urls import path
from vehiculo.views import index, consults, VehiculoList
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('index/', index, name='index'),
    path('consultas/', consults, name='consultas'),
    path('consult/', VehiculoList.as_view(), name='consultar'),
]
