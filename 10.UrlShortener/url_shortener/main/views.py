from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from .models import UrlPath
from django.contrib import messages
import random
import string


def generate_path(redirect_url, length=10):
    paths = UrlPath.objects.values_list("path", flat=True)

    full_string = string.digits + string.ascii_letters
    while True:
        current = "".join([random.choice(full_string) for _ in range(length)])
        if current not in paths:
            return current


def index(request: HttpRequest):
    if request.method == "POST":
        redirect_url = request.POST.get("redirect_url")
        # If that path already exists:
        existing_path = UrlPath.objects.filter(redirect_url=redirect_url).values_list("path", flat=True).first()
        if existing_path:
            return render(request, "index.html", {"path": f"{request.build_absolute_uri()}url/{existing_path}"})
        else:
            path = generate_path(redirect_url)
            new_url = UrlPath(path=path, redirect_url=redirect_url)
            new_url.save()
        messages.success(request, "Successfully created a url shortcut!")
        return render(request, "index.html", {"path": f"{request.build_absolute_uri()}url/{path}"})
    else:
        return render(request, "index.html")


def view(request, path):
    url_path = get_object_or_404(UrlPath, path=path)
    return redirect(url_path.redirect_url)
