from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from app.forms import LoginForm


# def loginView(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         try:
#             user = authenticate(username=form.data.get('username'), password=form.data.get('password'))
#             print(user)
#             if user is not None:
#                 login(request, user)
#                 return redirect('main')
#         except:
#             print("err")
#             form.add_error(None, 'Login error')
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})

class Login(LoginView):
    form_class = LoginForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('main')



def mainPageView(request):
    return render(request, 'main.html')