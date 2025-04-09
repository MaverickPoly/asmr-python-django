from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    tags = models.JSONField(default=list, blank=True)
    image = models.ImageField(upload_to="images/job/", null=False)
    author = models.ForeignKey(User, related_name="jobs", on_delete=models.CASCADE)
    accepted_users = models.ManyToManyField(User, related_name="accepted_jobs")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.author.username})"


class JobApply(models.Model):
    JOB_APPLY_STATUSES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("declined", "Declined"),
    ]

    job = models.ForeignKey(Job, related_name="applications", on_delete=models.CASCADE)
    comment = models.TextField(null=False)
    status = models.CharField(max_length=100, null=False, choices=JOB_APPLY_STATUSES)
    user = models.ForeignKey(User, related_name="applications", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Apply: ${self.job.title} - ${self.user.username}"
