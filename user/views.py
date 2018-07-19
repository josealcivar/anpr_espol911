from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView   # vista generica
from django.urls import reverse_lazy

from user.forms import RegistroUsersForm
# Create your views here.


class RegistroUsuario(CreateView):
     model = User
     template_name = 'user/register.html'
     form_class = RegistroUsersForm
     # form_class = UserCreationForm
     success_url = reverse_lazy('login')
