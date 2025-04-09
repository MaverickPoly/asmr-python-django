from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Account


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect("current_profile")
        else:
            if not User.objects.filter(username=username).exists():
                messages.warning(request, "Invalid username!")
            else:
                messages.warning(request, "Invalid password!")
            return redirect("login_view")
    else:
        return render(request, "login.html")


def register_view(request: HttpRequest):
    if request.method == "POST":
        # User Specific fields
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Account Specific fields
        profileImage = request.FILES.get("profileImage")
        account_type = request.POST.get("account_type")
        bio = request.POST.get("bio")
        links = get_list_data(request, "social_link_")
        location = request.POST.get("location")
        skills = None
        organization = None

        if account_type == "job_seeker":
            skills = get_list_data(request, "skill_")
        else:
            organization = request.POST.get("organization")
        
        # Checks
        if password != confirm_password:
            messages.warning(request, "Passwords do not match!")
            return redirect("register_view")
        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username is already taken!")
            return redirect("register_view")
        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email is already taken!")
            return redirect("register_view")
        
        new_user = User.objects.create_user(
            first_name=first_name, last_name=last_name, username=username, email=email, password=password
        )
        new_user.save()

        account = Account.objects.create(
            user=new_user, 
            profileImage=profileImage, 
            account_type=account_type, 
            bio=bio, 
            links=links, 
            location=location, 
            skills=skills, 
            organization=organization
        )
        account.save()
        messages.success(request, f"Account of type {account_type} created successfully")
        return redirect("login_view")
    else:
        return render(request, "register.html")
    

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("login_view")


@login_required
def change_password(request: HttpRequest):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # Checks
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("change_password_view")
        if not request.user.check_password(old_password):
            messages.error(request, "Invalid old password!")
            return redirect("change_password_view")
        
        request.user.set_password(new_password)
        request.user.save()
        messages.success(request, "Password changed successfully!")
        login(request, request.user)
        return redirect("landing_page")
    else:
        return render(request, "change_password.html")



# ======== Utility functions
def get_list_data(request, field_name):  # Gets list of data from form
    datas = []
    i = 1
    while True:
        key = f"{field_name}{i}"
        if key not in request.POST:
            break
        data = request.POST.get(key)
        if data:
            datas.append(data)
        i += 1

    return datas