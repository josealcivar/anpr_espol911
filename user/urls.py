from django.urls import path
from user.views import RegistroUsuario


urlpatterns = [
    path('registrar/', RegistroUsuario.as_view(), name='register'),
]
