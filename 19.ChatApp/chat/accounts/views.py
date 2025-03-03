from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Profile
from django.views.decorators.csrf import csrf_exempt


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email").strip()
        password = request.POST.get("password").strip()

        print(f"Email entered: {email}")
        print(f"Password entered: {password}")

        try:
            email_user = User.objects.get(email=email)
            print(f"User found: {email_user.username}")
            user = authenticate(request, username=email_user.username, password=password)
            print(f"Authenticated user: {user}")
        except Exception as e:
            print(f"Error retrieving user: {e}")
            user = None
        
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect("profile", user_id=user.id)
        else:
            messages.error(request, "Invalid credentials!")
            return redirect("login")
    
    return render(request, "login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username").strip()
        email = request.POST.get("email").strip()
        password = request.POST.get("password").strip()
        confirm_password = request.POST.get("confirm_password").strip()
        profile_image = request.FILES.get("profile_image", None)
        bio = request.POST.get("bio", "").strip()

        if User.objects.filter(username=username).exists():
            messages.error(request, "That username is already taken!")
            return redirect("register")
        if User.objects.filter(email=email).exists():
            messages.error(request, "That email is already taken!")
            return redirect("register")
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("register")
        
        user = User.objects.create_user(username=username, email=email, password=password)
        profile = Profile.objects.create(
            user=user,
            profile_image=profile_image,
            bio=bio
        )
        login(request, user)
        messages.success(request, "Registration successful! Account created!")
        return redirect("profile", user_id=user.id)
    else:
        return render(request, "register.html")
        

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")


@login_required
def change_password(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password").strip()
        password = request.POST.get("password").strip()
        confirm_password = request.POST.get("confirm_password").strip()

        if password != confirm_password:
            messages.error(request, "New passwords do not match!")
            return redirect("change_password")
        if not request.user.check_password(old_password):
            messages.error(request, "Invalid Old password!")
            return redirect("change_password")
        request.user.set_password(password)
        request.user.save()
        login(request, request.user)  # Else navigates to login page after changing password

        messages.success(request, "Password changed successfully!")
        return redirect("profile", user_id=request.user.id)
    else:
        return render(request, "change_password.html")
    

