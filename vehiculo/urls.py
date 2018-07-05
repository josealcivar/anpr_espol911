from django.urls import path
from vehiculo.views import index


urlpatterns = [
    path('index/', index, name='index'),
]
