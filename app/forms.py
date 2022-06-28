from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'exampleInputEmail1', 'aria-describedby': 'emailHelp'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control', 'id': 'exampleInputPassword1'}))


class PasswordChangeForm(forms.Form):
    password_old = forms.CharField(widget=forms.TextInput(attrs={'type': 'password', 'name': 'username', 'id': 'username', 'class': 'form-control'}))
    password_new = forms.CharField(widget=forms.TextInput(attrs={'type': 'password', 'name': 'password', 'id': 'password', 'class': 'form-control'}))
    password_retype = forms.CharField(widget=forms.TextInput(attrs={'type': 'password', 'name': 'password', 'id': 'password', 'class': 'form-control'}))
