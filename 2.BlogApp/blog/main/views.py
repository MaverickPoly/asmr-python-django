import os.path

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

import markdown
from .models import Profile, Post


@login_required(login_url="/auth/login/")
def index(request):
    posts = Post.objects.all().order_by("created_at")
    context = {
        "posts": posts
    }
    return render(request, "index.html", context)


@login_required(login_url="/auth/login/")
def create_blog(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get("content")
        image = request.FILES.get("image")
        author = request.user.profile
        post = Post.objects.create(author=author, title=title, content=content, image=image)
        messages.success(request, "Post created successfully!")
        return redirect("home")
    else:
        return render(request, "create_blog.html")


@login_required(login_url="/auth/login/")
def post_details(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    md_html = markdown.markdown(post.content)
    context = {
        "post": post,
        "md_html": md_html,
    }
    return render(request, "post_details.html", context)


@login_required(login_url="/auth/login/")
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author.user:
        if request.method == "POST":
            title = request.POST.get('title')
            content = request.POST.get('content')
            image = request.FILES.get('image')

            if image:
                print(f"Image path: {post.image.path}")
                print(f"Image url: {post.image.url}")
                if post.image and os.path.isfile(post.image.path):
                    os.remove(post.image.path)
                post.image = image

            post.title = title
            post.content = content
            post.save()

            messages.success(request, "Post updated successfully!")
            return redirect("blog_details", post_id=post_id)
        else:
            context = {"post": post}
            return render(request, "edit_post.html", context)
    else:
        messages.error(request, "You do not own that post!")
        return redirect("blog_details", post_id=post_id)


@require_http_methods(["DELETE"])
@login_required(login_url="/auth/login/")
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user == post.author.user:
        if post.image and os.path.isfile(post.image.path):
            os.remove(post.image.path)
        post.delete()
        return JsonResponse({"message": "Post deleted successfully!"}, status=200)
    else:
        return JsonResponse({"error": "You do not have permission to delete this post!"}, status=403)


# General

def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


@login_required(login_url="/auth/login/")
def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = user.profile
    print("Profile:", profile)
    context = {
        "current_user": user,
        "profile": profile
    }
    return render(request, "profile.html", context)


@login_required(login_url="/auth/login/")
def edit_profile(request):
    if request.method == "POST":
        bio = request.POST.get("bio")
        city = request.POST.get("city")
        profile_image = request.FILES.get("profile_image")

        user = request.user
        user.profile.bio = bio
        user.profile.city = city
        user.profile.profile_image = profile_image
        user.profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("profile", user.id)
    else:
        return render(request, "edit_profile.html")


@login_required(login_url="/auth/login/")
def user_followers(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = user.profile
    followers = profile.followers.all()
    context = {
        "current_user": user,
        "profile": profile,
        "followers": followers
    }
    return render(request, "followers_list.html", context)


# Utils
@require_http_methods(["POST"])
@login_required(login_url="/auth/login/")
def follow_unfollow(request, user_id):
    profile_to_follow = get_object_or_404(Profile, user__id=user_id)
    current_user_profile = request.user.profile

    if current_user_profile.user == profile_to_follow.user:
        messages.error(request, "You cannot follow yourself!")
        return JsonResponse({"success": False, "message": "You cannot follow yourself!"})

    if request.user in profile_to_follow.followers.all():
        profile_to_follow.followers.remove(request.user)
        is_following = False
    else:
        profile_to_follow.followers.add(request.user)
        is_following = True
    return JsonResponse({"success": True, "is_following": is_following, "followersCount": profile_to_follow.followers.count()})


@require_http_methods(["POST"])
@login_required(login_url="/auth/login/")
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    profile = request.user.profile

    if profile == post.author:
        messages.error(request, "You cannot like your own post!")
        return JsonResponse({"success": False, "message": "You cannot like your own post!"})

    if profile in post.likes.all():
        post.likes.remove(profile)
        liked = False
    else:
        post.likes.add(profile)
        liked = True
    return JsonResponse({"success": True, "liked": liked, "likes_count": post.likes.count()})


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
            messages.success(request, "Logged user in successfully!")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials!")
            return redirect("login")
    else:
        return render(request, "auth/login.html") 


@login_required(login_url="/auth/login/")
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")


def signup_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        profile_image = request.FILES.get("profile_image")
        bio = request.POST.get("bio")
        city = request.POST.get("city")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("signup")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("signup")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect("signup")
        user = User.objects.create(username=username, email=email, password=password)
        profile = Profile.objects.create(user=user, bio=bio, profile_image=profile_image, city=city)
        login(request, user)
        messages.success(request, "Signed up successfully!")
        return redirect("home")
    else:
        return render(request, "auth/signup.html")


@login_required(login_url="/auth/login/")
def change_password(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        if new_password != confirm_password:
            messages.error(request, "New Passwords do not match!")
            return redirect("change_password")
        if request.user.check_password(old_password):
            messages.error(request, "Invalid password")
            return redirect("change_password")
        request.user.set_password(new_password)
        request.user.save()
        messages.success(request, "Updated password successfully!")
        return redirect("home")
    else:
        return render(request, "auth/change_password.html")

