from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.views.decorators.http import require_http_methods
import json

from .models import *


@login_required(login_url="/login")
def index(request):
    todos = Todo.objects.filter(user=request.user).order_by("created_at")
    print(request.user.todos.all())
    return render(request, "index.html", {"todos": todos})


@login_required(login_url="/login")
def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        todo = Todo(title=title, description=description, user=request.user)
        todo.save()
        return redirect("home")
    else:
        return render(request, "create.html")


@require_http_methods(["DELETE"])
@login_required(login_url="/login")
def delete(request: HttpRequest):
    try:
        body = json.loads(request.body)
        todo_id = body.get("id")

        todo = Todo.objects.get(id=todo_id, user=request.user)
        todo.delete()
        return JsonResponse({"success": True, "message": "Todo deleted successfully!"})
    except Todo.DoesNotExist:
        return JsonResponse({"success": False, "message": "Todo not found!"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=400)



@require_http_methods(["PATCH"])
@login_required(login_url="/login")
def toggle_complete(request):
    try:
        body = json.loads(request.body)
        todo_id = body.get("id")
        completed = body.get("completed")

        todo = Todo.objects.get(id=todo_id, user=request.user)
        todo.completed = completed
        todo.save()
        return JsonResponse({"success": True, "message": "Todo updated successfully!"})
    except Todo.DoesNotExist:
        return JsonResponse({"success": False, "message": "Todo not found!"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=400)


@login_required(login_url="/login")
def update(request, todo_id):
    todo = Todo.objects.filter(id=todo_id).first()
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        completed = request.POST.get("completed")
        print(completed)
        if todo:
            todo.title = title
            todo.description = description
            todo.completed = completed == "on"
            todo.save()
        return redirect("home")
    else:
        return render(request, "update.html", {"todo": todo})


@login_required(login_url="/login")
def todo_details(request, todo_id):
    try:
        todo = Todo.objects.get(id=todo_id, user=request.user)
        return render(request, "todo_details.html", {"todo": todo})
    except Todo.DoesNotExist:
        messages.error(request, "Todo does not exist!")
        return redirect("home")
    except Exception as e:
        messages.error(str(e))
        return redirect("home")


def profile(request):
    todos = request.user.todos.all()
    return render(request, "profile.html", {"todos": todos})


# --- Auth ----

def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            email_user = User.objects.get(email=email)
            user = authenticate(request, username=email_user.username, password=password)
        except:
            user = None
        print(user)
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
            messages.error(request, "Username is already taken!")
            return redirect("register")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already taken!")
            return redirect("register")

        user = User.objects.create(username=username, password=make_password(password), email=email)
        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect("home")
    else:
        return render(request, "register.html")


@login_required(login_url="/login")
def logout_user(request):
    logout(request)
    messages.success(request, "You have beeb logged out successfully!")
    return redirect("login")
