from django.urls import path
from vehiculo.views import index, VehiculoList, VehiculoDenunciar, VehiculoChart, VehiculoReportadoList
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # path('index/', index, name='index'),
    path('index/', VehiculoChart.as_view(), name='index'),
    path('consultas/', VehiculoList.as_view(), name='consultar'),
    path('consultas/denunciar/<int:pk>', VehiculoDenunciar.as_view(), name='reportar_vehiculo'),
    path('reportados/', VehiculoReportadoList.as_view(), name='vehiculos_reportados'),
]
