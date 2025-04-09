from django.shortcuts import render
from django.contrib import messages



def home(request):
    context = {
        # "messages": ["Hello world"]
    }
    return render(request, "home.html", context)
