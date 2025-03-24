from django.db import models
from django.contrib.auth.models import User


class Poll(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, related_name="polls", on_delete=models.CASCADE)

    def __str__(self):
        return self.title



class Question(models.Model):
    title = models.CharField(max_length=300)
    poll = models.ForeignKey(Poll, related_name="questions", on_delete=models.CASCADE)


    def __str__(self):
        return self.title
    

class PollResult(models.Model):
    poll = models.ForeignKey(Poll, related_name="results", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="completed_polls", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} completed {self.poll}"
    

class Answer(models.Model):
    user = models.ForeignKey(User, related_name="answers", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    answer = models.TextField()

    def __str__(self):
        return f"{self.user} answered {self.question}"
