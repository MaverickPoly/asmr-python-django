from http.client import HTTPResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate


@login_required()
def index(request):
    return render(request, "index.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Logged in successfully as {user.username}")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password!")
            return redirect("login")
    else:
        return render(request, "login.html")


def signup_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already in use!")
            return redirect("signup")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use!")
            return redirect("signup")
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("signup")
        user = User(username=username, email=email, password=make_password(password))
        user.save()
        login(request, user)
        messages.success(request, "Signed up successfully!")
        return redirect("home")
    else:
        return render(request, "signup.html")


def github_auth(request):
    return render(request, "github.html")


@login_required()
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")
