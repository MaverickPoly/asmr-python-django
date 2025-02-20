from django.db import models
from django.contrib.auth.models import User



class Todo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user: User = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todos")

    def __str__(self):
        return f"{self.title} - {self.user.username}"
