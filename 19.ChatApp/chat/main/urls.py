from django.urls import path
from . import views


urlpatterns = [
    # Chat Functionality
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("chats/", views.all_chats, name="all_chats"),
    path("chat/<int:chat_id>/", views.chat, name="chat"),
    path("chat/<int:chat_id>/delete/", views.delete_chat, name="delete_chat"),
    path("chat/<int:chat_id>/details/", views.chat_details, name="chat_details"),
    path("chat/<int:chat_id>/register/", views.register_chat, name="register_chat"),
    path("chat/create/", views.create_chat, name="create_chat"),

    # Message
    path("message/<int:message_id>/delete/", views.delete_message, name="delete_message"),

    # Profile
    path("profile/<int:user_id>/", views.profile, name="profile"),
]
