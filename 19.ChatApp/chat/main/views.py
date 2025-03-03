from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Chat, Message
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse


# View all chats in which we take part
@login_required
def home(request):
    chats = Chat.objects.filter(participants=request.user)
    context = {
        "chats": chats
    }
    return render(request, "home.html", context)


# Profile of different users
@login_required
def profile(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    target_profile = target_user.profile
    context = {
        "target_user": target_user,
        "target_profile": target_profile,
    }
    return render(request, "profile.html", context)


# Search for users
@login_required
def search(request):
    query = request.GET.get("query", "").strip().lower()
    filter_tag = request.GET.get("filter", "")
    print(f"Query: {query}")
    print(f"Filter Tag: {filter_tag}")
    if filter_tag == "users":
        users = User.objects.filter(username__icontains=query) | User.objects.filter(email__icontains=query)
        context = {
            "users": users,
        }
        print(f"Users: {len(users)}")
        return render(request, "search.html", context)
    elif filter_tag == "chats":
        chats = Chat.objects.filter(title__icontains=query)
        context = {
            "chats": chats,
        }
        print(f"Chats: {len(chats)}")
        return render(request, "search.html", context)
    return render(request, "search.html")
        

# Display all the messages from users belonging to that chat, with form for writing message
@login_required
def chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    if request.user not in chat.participants.all():
        messages.error(request, "You are not participating in that chat!")
        return redirect("home")  # User is not part of the chat
    
    if request.method == "POST":
        content = request.POST.get("content")
        Message.objects.create(chat=chat, author=request.user, content=content)
        messages.success(request, "Message sent successfully!")
        return redirect("chat", chat_id=chat.id)
    else:
        sent_msgs = chat.messages.order_by("created_at")
        context = {
            "chat": chat,
            "sent_msgs": sent_msgs
        }
        return render(request, "chat.html", context)


# Micro
@login_required
def delete_chat(request, chat_id):
    """Delete the current user from the chat participants"""
    chat = get_object_or_404(Chat, id=chat_id)

    if request.user in chat.participants.all():
        chat.participants.remove(request.user)
        messages.success(request, "You left the chat successfully!")
        if chat.participants.count() == 0:
            chat.delete()
    return redirect("home")


# Delete message
@login_required
@require_http_methods(["DELETE"])
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.user == message.author:
        message.delete()
        messages.success(request, "Message deleted successfully!")
        return JsonResponse({"success": True, "message": "Message deleted successfully!"})
    else:
        messages.error(request, "You cannot delete this message as you do not own this!")
        return JsonResponse({"success": False, "error": "You cannot delete this message, cuz you do not own it!"}, status=403)


# All Chats, existent
@login_required
def all_chats(request):
    chats = Chat.objects.order_by("created_at")
    context = {
        "chats": chats
    }
    return render(request, "chats.html", context)


# About Chat, participants date etc...
@login_required
def chat_details(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    if request.user not in chat.participants.all():
        return redirect("home")

    return render(request, "chat_details.html", {"chat": chat})


# Person joins a chat
@login_required
@require_http_methods(["POST"])
def register_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    if request.user in chat.participants.all():
        return JsonResponse({"success": False, "error": "Already a participant"}, status=400)

    chat.participants.add(request.user)
    messages.success(request, "You was registered to chat!")
    return JsonResponse({"success": True, "message": "Successfully registered to a chat!"})


@login_required
def create_chat(request):
    if request.method == "POST":
        title = request.POST.get("title")
        chat_image = request.FILES.get("chat_image")
        chat = Chat.objects.create(title=title, chat_image=chat_image)
        chat.participants.add(request.user)
        messages.success(request, "Chat created successfully!")
        return redirect("chat", chat_id=chat.id)
    else:
        return render(request, "create_chat.html")
    