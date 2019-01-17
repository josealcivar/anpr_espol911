from django.urls import path
from vehiculo.views import index, VehiculoList, VehiculoDenunciar, VehiculoChart, VehiculoReportadoList, ProfileCar, ReportadoDelete
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # path('index/', index, name='index'),
    path('index/', login_required(VehiculoChart.as_view()), name='index'),
    path('consultas/', login_required(VehiculoList.as_view()), name='consultar'),
    path('consultas/perfil/<int:pk>', login_required(ProfileCar.as_view()), name='perfil'),
    path('consultas/denunciar/<int:pk>', login_required(VehiculoDenunciar.as_view()), name='reportar_vehiculo'),
    path('reportados/', login_required(VehiculoReportadoList.as_view()), name='vehiculos_reportados'),
    path('reportados/eliminar/<int:pk>', login_required(ReportadoDelete.as_view()), name='eliminar_reportado'),
]
