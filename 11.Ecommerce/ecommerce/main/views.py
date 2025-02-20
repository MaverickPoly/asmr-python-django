from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods

from .models import Product
import json


@login_required(login_url="/login")
def home(request):
    products = Product.objects.all().order_by("created_at")
    cart_ids = request.session.get("cart", [])
    context = {
        "products": products,
        "cart_ids": cart_ids,
    }
    return render(request, "index.html", context)


@login_required(login_url="/login")
def cart(request):
    try:
        cart_ids = request.session.get("cart", [])
        products = []
        total_price = 0
        for cart_id in cart_ids:
            product = Product.objects.get(id=cart_id)
            products.append(product)
            total_price += product.price
        context = {
            "products": products,
            "cart_ids": cart_ids,
            "total_price": total_price
        }
        return render(request, "cart.html", context)
    except:
        messages.error(request, "Invalid cart!")


@login_required(login_url="/login")
def about(request):
    return render(request, "about.html")


@login_required(login_url="/login")
def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "product_details.html", {"product": product})


@login_required(login_url="/login")
def create_product(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        image_file = request.FILES.get("image_file")
        product = Product(name=name, description=description, price=price, quantity=quantity, image_file=image_file)
        product.save()
        messages.success(request, "Product created successfully!")
        return redirect("home")
    else:
        return render(request, "create_product.html")


@login_required(login_url="/login")
def profile(request):
    return render(request, "profile.html")


@require_http_methods(["PATCH"])
@login_required(login_url="/login")
def add_to_cart(request):
    try:
        body = json.loads(request.body)
        product_id = body.get("id")
        product = get_object_or_404(Product, id=product_id)
        cart = request.session.get("cart", [])
        if product.id in cart:
            messages.error(request, "Product already in cart!")
            return JsonResponse({"success": False, "message": f"Product {product.name} already in cart!"})
        else:
            cart.append(product.id)
            request.session["cart"] = cart
            messages.success(request, f"Item {product.name} added to cart successfully!")
            return JsonResponse({"success": True, "message": f"Added {product.name} to cart successfully!"})
    except Exception as e:
        return JsonResponse({"success": False, "message": f"Error: {e}"})


@require_http_methods(["PATCH"])
@login_required(login_url="/login")
def remove_from_cart(request):
    try:
        body = json.loads(request.body)
        product_id = body.get("id")
        product = get_object_or_404(Product, id=product_id)
        cart = request.session.get("cart", [])
        if product.id in cart:
            cart.remove(product.id)
            request.session["cart"] = cart
            messages.success(request, f"Item {product.name} removed from cart successfully!")
            return JsonResponse({"success": True, "message": f"Removed {product.name} from cart successfully!"})
        else:
            messages.error(request, "Item does not exist in cart!")
            return JsonResponse({"success": False, "message": f"Item {product.name} does not exist in cart!"})
    except Exception as e:
        return JsonResponse({"success": False, "message": f"Error: {e}!"})


@require_http_methods(["PATCH"])
@login_required(login_url="/login")
def delete_product(request):
    try:
        body = json.load(request.body)
        product_id = body.get("id")
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return JsonResponse({"success": True, "message": "Product deleted successfully!"})
    except Exception as e:
        return JsonResponse({"success": False, "message": f"Error: {e}"})


# Auth

def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            email_user = User.objects.get(email=email)
            user = authenticate(request, username=email_user.username, password=password)
        except:
            user = None

        if user:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect("home")
        else:
            messages.error(request, "Email or password incorrect!")
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
            messages.error(request, "Username already taken!")
            return redirect("register")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already taken!")
            return redirect("register")

        user = User(username=username, email=email, password=make_password(password))
        user.save()
        login(request, user)
        messages.success(request, "Created account successfully!")
        return redirect("home")
    else:
        return render(request, "register.html")


@login_required(login_url="/login")
def logout_user(request):
    messages.success(request, "Logged out successfully!")
    logout(request)
    return redirect("login")
