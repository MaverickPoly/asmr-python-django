from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .models import Profile, Quiz, Question



@login_required(login_url="/login")
def index(request):
    quizzes = Quiz.objects.all().order_by("created_at")
    context = {
        "quizzes": quizzes,
    }
    return render(request, "index.html", context)


@login_required(login_url="/login")
def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        total_questions = int(request.POST.get("total_questions"))

        quiz = Quiz.objects.create(title=title, total_questions=total_questions, user=request.user)

        for i in range(1, total_questions + 1):
            question_text = request.POST.get(f"question_{i}")
            answer_1 = request.POST.get(f"answer_1_{i}")
            answer_2 = request.POST.get(f"answer_2_{i}")
            answer_3 = request.POST.get(f"answer_3_{i}")
            answer_4 = request.POST.get(f"answer_4_{i}")
            correct_answer = int(request.POST.get(f"correct_answer_{i}"))

            Question.objects.create(
                quiz=quiz,
                question=question_text,
                answer_1=answer_1,
                answer_2=answer_2,
                answer_3=answer_3,
                answer_4=answer_4,
                correct_answer=correct_answer,
            )
        messages.success(request, "Quiz created successfully!")
        return redirect("home")
    else:
        return render(request, "create.html")


@login_required(login_url="/login")
def practice_quiz(request, id):
    quiz = get_object_or_404(Quiz, id=id)
    questions = quiz.questions.all()
    context = {
        "quiz": quiz,
        "questions": questions
    }
    return render(request, "practice_quiz.html", context)


@login_required(login_url="/login")
def quiz_result(request: HttpRequest, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    correct_count = 0
    total_questions = questions.count()

    for question in questions:
        selected_answer = request.POST.get(f"question_{question.id}")
        if selected_answer and int(selected_answer) == question.correct_answer:
            correct_count += 1

    score = int(round((correct_count / total_questions) * 100, 2))
    messages.success(request, f"Quiz Completed! Your score is: {score}%")
    quiz = get_object_or_404(Quiz, id=quiz_id)
    request.user.profile.total_quizzes += 1
    request.user.profile.save()
    context = {
        "quiz": quiz,
        "score": score
    }
    return render(request, "quiz_result.html", context)


# General
@login_required(login_url="/login")
def about(request):
    return render(request, "about.html")


@login_required(login_url="/login")
def profile(request):
    return render(request, "profile.html")


@login_required(login_url="/login")
def edit_profile(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        bio = request.POST.get("bio")

        request.user.username = username
        request.user.email = email
        request.user.profile.bio = bio
        request.user.save()
        request.user.profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("profile")
    else:
        return render(request, "edit_profile.html")



# Authentication
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
            messages.success(request, "Logged in successfully!")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials!")
            return redirect("login")
    else:
        return render(request, "auth/login.html")



def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        bio = request.POST.get("bio")
        profile_img = request.FILES.get("profile_img")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("register")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("register")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already registered!")
            return redirect("register")
        user = User.objects.create(email=email, username=username, password=make_password(password))
        profile = Profile.objects.create(user=user, profile_picture=profile_img, bio=bio)
        login(request, user)
        messages.success(request, "Signed up successfully!")
        return redirect("home")
    else:
        return render(request, "auth/register.html")


@login_required(login_url="/login")
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")

