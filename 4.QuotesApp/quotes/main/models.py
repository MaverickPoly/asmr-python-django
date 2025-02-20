from django.db import models
from django.contrib.auth.models import User


class Quote(models.Model):
    author: User = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quotes")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    favourited_by = models.ManyToManyField(User, related_name="favourite_quotes", blank=True)

    def __str__(self):
        return f"{self.content[:30]} - {self.author.username}"
