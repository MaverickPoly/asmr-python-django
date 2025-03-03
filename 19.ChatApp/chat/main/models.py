from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(User, related_name="chats")
    title = models.CharField(max_length=200)
    chat_image = models.ImageField(upload_to="images/chat/", default="images/chat/default.png")

    def __str__(self):
        return f"{self.title} - {len(self.participants)} users"


class Message(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    created_at = models.DateTimeField(auto_now_add=True)
