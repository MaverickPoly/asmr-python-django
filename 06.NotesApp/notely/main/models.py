from django.contrib.auth.models import User
from django.db import models



class Note(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    tag = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user: User = models.ForeignKey(User, related_name="notes", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.user.username}"
