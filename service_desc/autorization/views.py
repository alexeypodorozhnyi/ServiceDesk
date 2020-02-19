from django.contrib.auth.views import LoginView, LogoutView

from django.shortcuts import redirect
from django.views.generic import CreateView
from .forms import RegisterForm
from django.contrib.auth.models import User


class Login(LoginView):
    http_method_names = ['get', 'post']
    redirect_authenticated_user = True
    template_name = 'autorization/login.html'
    success_url = '/'


class Logout(LogoutView):
    http_method_names = ['get']
    success_url = '/'

    def get(self, *args, **kwargs):
        super().get(*args, **kwargs)
        return redirect('/')


class Register(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'autorization/register.html'
    success_url = '/'
