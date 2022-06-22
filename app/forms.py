from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'exampleInputEmail1', 'aria-describedby': 'emailHelp'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control', 'id': 'exampleInputPassword1'}))
   # class Meta:
   #      model = User
   #      fields = ['username', 'password']
   #      widgets = {
   #          'username': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'exampleInputEmail1', 'aria-describedby': 'emailHelp'}),
   #          'password': forms.TextInput(attrs={'type': 'password', 'class': 'form-control', 'id': 'exampleInputPassword1'}),
   #      }