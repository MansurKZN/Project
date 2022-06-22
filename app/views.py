from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from app.forms import LoginForm, PasswordChangeForm


class Login(LoginView):
    form_class = LoginForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('main')

def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def mainPageView(request):
    user = request.user.username
    return render(request, 'main.html', {"user": user})


class Profie(View):

    def get(self, request):
        user = request.user.username
        form = PasswordChangeForm()
        return render(request, 'profile.html', {"user": user, 'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.POST)
        user = request.user
        message = ''
        error = ''
        if user.check_password(form.data.get('password_old')):
            if form.data.get('password_new') == form.data.get('password_retype'):
                user.set_password(form.data.get('password_new'))
                user.save()
                message = 'Password changed successfully'
            else:
                error = 'New password and retype password not equal'
                form.add_error(None, 'Password change error')
        else:
            error = 'Old password is incorrect'
            form.add_error(None, 'Password change error')
        return render(request, 'profile.html', {"user": user, 'form': form, 'message': message, 'error': error})



