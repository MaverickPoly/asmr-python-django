from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from .models import Book, Comment
import json


@login_required(login_url="/login")
def about(request):
    return render(request, "about.html")


@login_required(login_url="/login")
def index(request):
    books = Book.objects.all().order_by("uploaded_at")
    category_choices = Book.category_choices
    context = {
        "books": books,
        "category_choices": category_choices,
    }
    return render(request, "index.html", context)


@login_required(login_url="/login")
def create_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        file = request.FILES.get('file')
        written_date = request.POST.get('written_date')
        author = request.POST.get("author")
        tag = request.POST.get("tag")

        book = Book(title=title, file=file, written_date=written_date , author=author, tag=tag)
        book.save()

        messages.success(request, f"Created book {title} successfully!")
        return redirect("home")
    else:
        category_choices = Book.category_choices
        return render(request, "create_book.html", {"category_choices": category_choices})


@login_required(login_url="/login")
def update_book(request):
    pass


@login_required(login_url="/login")
def delete_book(request):
    pass


@login_required(login_url="/login")
def search_book(request):
    if request.method == "POST":
        query = request.POST.get("query")
        books = Book.objects.filter(title__icontains=query) | Book.objects.filter(author__icontains=query)
        context = {"books": books, "query": query}
        return render(request, "search_results.html", context)
    return redirect("home")
    


# Get all books with the tag.
@login_required(login_url="/login")
def filter_tag(request, tag):
    books = Book.objects.filter(tag=tag).order_by("uploaded_at")
    return render(request, "tag_books.html", {"books": books, "tag": tag})


@login_required(login_url="/login")
def profile(request, profile_id):
    user = get_object_or_404(User, id=profile_id)
    return render(request, "profile.html", {"user_profile": user})


@require_http_methods(["PATCH"])
@login_required(login_url="/login")
def borrow_book(request):
    try:
        body = json.loads(request.body);
        book_id = body.get("id");
        book: Book = Book.objects.get(id=book_id);
        if book.borrower:
            messages.error(request, "This book is already borrowed!")
            return JsonResponse({"success": False, "message": "This book is already borrowed!"})
        else:
            book.borrower = request.user
            book.save()
            messages.success(request, f"Borrowed book {book.title} successfully!")
            return JsonResponse({"success": True, "message": f"Borrowed book {book.title} successfully!"})

    except Book.DoesNotExist:
        return JsonResponse({"success": False, "message": "Book not found!"});
    except Exception as e:
        return JsonResponse({"success": False, "message": f"Error: {e}"});


@require_http_methods(["PATCH"])
@login_required(login_url="/login")
def return_book(request):
    try:
        body = json.loads(request.body)
        book_id = body.get("id")
        book: Book = Book.objects.get(id=book_id);
        if book.borrower:
            if book.borrower != request.user:
                messages.error(request, "You cannot return the book that you have not borrowed!")
                return JsonResponse({"success": False, "message": "You cannot return the book that you have not borrowed!"})
            book.borrower = None
            book.save()
            messages.success(request, f"The book {book.title} successfully returned!")
            return JsonResponse({"success": True, "message": f"The book {book.title} successfully returned!"})
        else:
            messages.error(request, "The book is not yet borrowed!")
            return JsonResponse({"success": False, "message": "The book is not yet borrowed!"})
    except Book.DoesNotExist:
        return JsonResponse({"success": False, "message": "Book not found!"});
    except Exception as e:
        return JsonResponse({"success": False, "message": f"Error: {e}"});


@login_required(login_url="/login")
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, "book_detail.html", {"book": book})


@login_required(login_url="/login")
def comments(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        content = request.POST.get("content")
        comment = Comment(content=content, author=request.user, book=book)
        comment.save()
        messages.success(request, f"Wrote comment successfully on book: {book.title}")
        return redirect("book_comments", book_id=book_id)
    else:
        return render(request, "book_comments.html", {"book": book})


# ------ AUTH -----

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
            messages.error(request, "Username already registered!")
            return redirect("register")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("register")

        user = User(username=username, email=email, password=make_password(password))
        user.save()
        login(request, user)
        messages.success(request, "Account successfully created!")
        return redirect("home")
    else:
        return render(request, "register.html")


@login_required(login_url="/login")
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")


@login_required(login_url="/login")
def change_password(request):
    pass

