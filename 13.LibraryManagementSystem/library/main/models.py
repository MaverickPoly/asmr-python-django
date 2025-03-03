from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    category_choices = [
        ('education', 'Education'),
        ('sci-fi', 'Sci-Fi'),
        ('fantasy', 'Fantasy'),
        ('mystery', 'Mystery'),
        ('romance', 'Romance'),
        ('biography', 'Biography'),
        ('history', 'History'),
        ('self-help', 'Self-Help'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=300)
    file = models.FileField(upload_to="uploads/")
    written_date = models.DateField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=300)
    tag = models.CharField(max_length=200, choices=category_choices)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="borrowed_books", null=True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    written_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="comments")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.author.username}, {self.book.title} - {self.content[:50]}"

