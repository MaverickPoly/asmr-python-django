from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib import messages

import json
from .models import Note
from . import forms
import markdown


# Create your views here.
@login_required(login_url="/login")
def index(request):
    # {% for note in user.notes %}
    return render(request, "index.html")


@login_required(login_url="/login")
def profile(request):
    return render(request, "profile.html")


@login_required(login_url="/login")
def create(request):
    if request.method == "POST":
        form = forms.NewNoteForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            content = form.cleaned_data.get("content")
            tag = form.cleaned_data.get("tag")

            note = Note(title=title, content=content, tag=tag, user=request.user)
            note.save()
            messages.success(request, "Note created successfully!")
            return redirect("home")
        else:
            messages.error(request, "Please fix the errors to proceed!")
            return redirect("create")
    else:
        form = forms.NewNoteForm()
        return render(request, "create.html", {"form": form})


@require_http_methods(["DELETE"])
@login_required(login_url="/login")
def delete_note(request: HttpRequest):
    try:
        body = json.loads(request.body)
        note_id = body.get("id")

        note = Note.objects.get(id=note_id, user=request.user)
        note.delete()
        return JsonResponse({"success": True, "message": "Note deleted successfully!"})
    except Note.DoesNotExist:
        return JsonResponse({"success": False, "message": "Note not found"})
    except Exception as e:
        return JsonResponse({"success": False, "message": f"Error: {e}"})


@login_required(login_url="/login")
def update_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        tag = request.POST.get("tag")
        note.title = title
        note.content = content
        note.tag = tag
        note.save()
        messages.success(request, "Note updated successfully!")
        return redirect("home")
    else:
        return render(request, "update_note.html", {"note": note})


@login_required(login_url="/login")
def note_details(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    content = markdown.markdown(note.content)
    return render(request, "note_details.html", {"note": note, "content": content})


@require_http_methods(["DELETE"])
@login_required(login_url="/login")
def clear_notes(request):
    Note.objects.filter(user=request.user).delete()
    messages.success(request, "Notes were cleared successfully!")
    return JsonResponse({"success": True, "message": "Notes cleared successfully!"})


# ------ Auth ------

def login_user(request):
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            try:
                email_user = User.objects.get(email=email)
                user = authenticate(request, username=email_user.username, password=password)
            except:
                user = None
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect("home")
            else:
                messages.error(request, "Invalid email or password")
                return redirect("login")
        else:
            return redirect("login")
    else:
        form = forms.LoginForm()
        return render(request, "login.html", {"form": form})


def register_user(request):
    if request.method == "POST":
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            confirm_password = form.cleaned_data.get("confirm_password")

            if password != confirm_password:
                messages.error(request, "Passwords do not match!")
                return redirect("register")
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already registered!")
                return redirect("register")
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered!")
                return redirect("register")

            user = User(username=username, email=email, password=make_password(password))
            user.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("home")
        else:
            return redirect("register")
    else:
        form = forms.RegisterForm()
        return render(request, "register.html", {"form": form})


@login_required(login_url="/login")
def logout_user(request: HttpRequest):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")
