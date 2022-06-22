from django import forms
from django.contrib.auth.forms import AuthenticationForm

from app.models import WorkReport, Project


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'exampleInputEmail1', 'aria-describedby': 'emailHelp'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control', 'id': 'exampleInputPassword1'}))


class PasswordChangeForm(forms.Form):
    password_old = forms.CharField(widget=forms.TextInput(attrs={'type': 'password', 'name': 'username', 'id': 'username', 'class': 'form-control'}))
    password_new = forms.CharField(widget=forms.TextInput(attrs={'type': 'password', 'name': 'password', 'id': 'password', 'class': 'form-control'}))
    password_retype = forms.CharField(widget=forms.TextInput(attrs={'type': 'password', 'name': 'password', 'id': 'password', 'class': 'form-control'}))


# class WorkReportForm(forms.Form):
    # class Meta:
    #     model = WorkReport
    #     fields = ['date', 'project', 'work_type', 'period', 'text']

    # all_proj = Project.objects.all()
    # projects = []
    # count = 0
    # for i in all_proj:
    #     count += 1
    #     a = (count, i.name)
    #     projects.append(a)
    #
    #
    # date = forms.CharField(widget=forms.TextInput(attrs={'type': 'datetime-local', 'id': 'datetime'}), required=True)
    # project = forms.ChoiceField(widget=forms.Select(), required=True, choices=projects)
    # work_type = forms.CharField(widget=forms.TextInput(attrs={'type': 'password', 'name': 'password', 'id': 'password', 'class': 'form-control'}))
    # engineer = forms.CharField(widget=forms.TextInput(attrs={'type': 'password', 'name': 'password', 'id': 'password', 'class': 'form-control'}))
    # period = forms.CharField(widget=forms.TextInput(attrs={'type': 'password', 'name': 'password', 'id': 'password', 'class': 'form-control'}))
    # text = forms.CharField(widget=forms.TextInput(attrs={'type': 'password', 'name': 'password', 'id': 'password', 'class': 'form-control'}))