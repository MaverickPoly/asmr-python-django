from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_picture = models.FileField(upload_to="profile_images/", blank=False, null=False)
    bio = models.TextField(max_length=1000)
    total_quizzes = models.IntegerField(default=0)  # Total quizzes completed

    def __str__(self):
        return f"{self.user.username} - {self.user.email}"


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="quizzes", on_delete=models.CASCADE)
    total_questions = models.IntegerField()

    def __str__(self):
        return f"{self.title} - {self.total_questions}"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    question = models.CharField(max_length=300)
    answer_1 = models.CharField(max_length=100)
    answer_2 = models.CharField(max_length=100)
    answer_3 = models.CharField(max_length=100)
    answer_4 = models.CharField(max_length=100)
    correct_answer = models.IntegerField(null=False)  # Correct answer index

    def __str__(self):
        return f"{self.question} -> {self.quiz.title}"



