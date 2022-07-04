from django import forms
from django.contrib.auth.forms import AuthenticationForm
from app.models import Manager


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'exampleInputEmail1', 'aria-describedby': 'emailHelp'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control', 'id': 'exampleInputPassword1'}))


class PasswordChangeForm(forms.Form):
    password_old = forms.CharField(widget=forms.TextInput(attrs={'type': 'password', 'name': 'username', 'id': 'username', 'class': 'form-control'}))
    password_new = forms.CharField(widget=forms.TextInput(attrs={'type': 'password', 'name': 'password', 'id': 'password', 'class': 'form-control'}))
    password_retype = forms.CharField(widget=forms.TextInput(attrs={'type': 'password', 'name': 'password', 'id': 'password', 'class': 'form-control'}))


class UserCreationForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = Manager
        fields = ('work_time', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
