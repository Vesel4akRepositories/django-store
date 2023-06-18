from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login as auth_login
from .forms import RegistrationForm, LoginForm


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            auth_login(request, user)
            return redirect('catalog')  # Редирект на вашу главную страницу после успешной регистрации
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('catalog')
            else:
                form.add_error(None, 'Invalid username or password')  # Add error to non-field error list
    else:
        form = LoginForm()
    
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')