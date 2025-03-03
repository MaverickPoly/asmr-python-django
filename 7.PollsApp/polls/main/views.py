from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User 
from django.views.decorators.http import require_http_methods

from . import models


@login_required(login_url="login_user")
def home(request):
    polls = models.Poll.objects.all().order_by("created_at")
    context = {
        "polls": polls,
    }
    return render(request, "index.html", context)



@login_required(login_url="login_user")
def create_poll(request):
    if request.method == "POST":
        title = request.POST.get("title")
        questions = request.POST.getlist('questions')

        if not questions or all(q.strip() == "" for q in questions):
            messages.error(request, "At least one question is required!")
            return redirect("create_poll")
        poll = models.Poll.objects.create(title=title, author=request.user)
        for question_text in questions:
            if question_text.strip():
                models.Question.objects.create(title=question_text, poll=poll)

        messages.success(request, "Poll created successfully!")
        return redirect("home")
    else:
        return render(request, "create_poll.html")


@login_required(login_url="login_user")
def solve_poll(request, poll_id):
    poll: models.Poll = get_object_or_404(models.Poll, id=poll_id)
    questions = poll.questions.all()

    if models.PollResult.objects.filter(poll=poll, user=request.user).exists():
        messages.info(request, "You have already answered this poll.")
        return redirect("home")
    
    if request.method == "POST":
        for question in questions:
            answer_text = request.POST.get(f"question_{question.id}").strip()
            if answer_text:
                models.Answer.objects.create(user=request.user, question=question, answer=answer_text)
        models.PollResult.objects.create(poll=poll, user=request.user)

        messages.success(request, "Poll submitted successfully!")
        return redirect("home")
    else:
        context = {
            "poll": poll,
            "questions": questions
        }
        return render(request, "solve_poll.html", context)


@login_required(login_url="login_user")
def poll_users(request, poll_id):
    poll = get_object_or_404(models.Poll, id=poll_id)
    completed_users = models.PollResult.objects.filter(poll=poll).select_related("user")
    context = {
        "poll": poll,
        "completed_users": completed_users
    }
    return render(request, "poll_users.html", context)


@require_http_methods(["PATCH"])
@login_required(login_url="login_user")
def delete_poll(request):
    pass


@login_required(login_url="login_user")
def profile(request):
    return render(request, "profile.html")


# Authentication

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Logged in successfully as {username}")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials!")
            return redirect("login_user")
    else:
        return render(request, "login.html")


@login_required(login_url="login_user")
def logout_user(request):
    logout(request)
    messages.success(request, "User logged out successfully!")
    return redirect("login_user")


def signup_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("signup_user")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("signup_user")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect("signup_user")
        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Signed up successfully!")
        return redirect("login_user")
    else:
        return render(request, "signup.html")
