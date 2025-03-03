from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods

from .models import Quote



@login_required(login_url="/login")
def index(request):
    quotes = Quote.objects.all().order_by("created_at")
    return render(request, "index.html", {"quotes": quotes})


@login_required(login_url="/login")
def create(request):
    if request.method == "POST":
        content = request.POST.get("content")
        quote = Quote(content=content, author=request.user)
        quote.save()
        messages.success(request, "Quote created successfully!")
        return redirect("home")
    else:
        return render(request, "create.html")



@login_required(login_url="/login")
def profile(request):
    return render(request, "profile.html")


@login_required(login_url="/login")
def read_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    return render(request, "read_quote.html", {"quote": quote})


@require_http_methods(["PATCH"])
@login_required(login_url="/login")
def toggle_favourite(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    if quote.favourited_by.filter(id=request.user.id).exists():
        quote.favourited_by.remove(request.user)
        return JsonResponse({"success": True, "favourited": False, "message": "Quote removed from favourites"})
    else:
        quote.favourited_by.add(request.user)
        return JsonResponse({"success": True, "favourited": False, "message": "Quote removed from favourites"})


# ----- Auth -----


def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            email_user = User.objects.get(email=email)
            user = authenticate(request, username=email_user.username, password=password)
        except:
            user = None

        if user is not None:
            login(request, user)
            messages.success(request, "You logged in successfully!")
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password!")
            return redirect("login")

    else:
        return render(request, "login.html")


def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("register")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already in use!")
            return redirect("register")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use!")
            return redirect("register")

        user = User.objects.create(username=username, email=email, password=make_password(password))
        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect("home")
    else:
        return render(request, "register.html")


@login_required(login_url="/login")
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")

