from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm, SignUpForm


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=request.POST['username'],
                password=request.POST['password']
            )

            if user and user.is_active:
                login(request, user)
                return redirect('home')

        else:
            return render(request, 'accounts/login.html', {'form': form})

    else:
        return render(request, 'accounts/login.html', {'form': LoginForm()})


def logout_view(request):
    logout(request)
    return redirect('auth:login')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=request.POST['username'],
                email=request.POST['email'],
                password=request.POST['password']
            )
            return redirect('auth:login')
        else:
            return render(request, 'accounts/signup.html', {'form': form})

    else:
        return render(request, 'accounts/signup.html', {'form': SignUpForm()})
