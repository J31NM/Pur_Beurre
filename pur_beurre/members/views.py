from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from .models import *
from .forms import CreateUserForm

class UserRegisterView(generic.CreateView):
    form_class = CreateUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class UserLoginView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')

class UserAccountView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/user_account.html'
    success_url = reverse_lazy('home')
