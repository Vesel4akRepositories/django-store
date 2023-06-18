from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=255, required=True)
    surname = forms.CharField(max_length=255, required=True)
    patronymic = forms.CharField(max_length=255, required=False)
    login = forms.CharField(max_length=255, required=True, unique=True)
    email = forms.EmailField(required=True, unique=True)
    password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['name', 'surname', 'patronymic', 'login', 'email', 'password1', 'password2']


