from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Account(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ("job_seeker", "Job Seeker"),
        ("employer", "Employer"),
    ]

    user = models.ForeignKey(User, related_name="account", on_delete=models.CASCADE)

    profileImage = models.ImageField(upload_to="images/profile/", blank=True, default="media/images/profile/default.png")
    account_type = models.CharField(max_length=200, null=False, choices=ACCOUNT_TYPE_CHOICES)  # 'job_seeker' | 'employer'
    bio = models.CharField(max_length=1000, null=False)
    links = models.JSONField(default=list, blank=True)  # Social Links field
    location = models.CharField(max_length=200)

    # Job Seeker Specific
    skills = models.JSONField(default=list, blank=True, null=True)

    # Employer Specific
    organization = models.CharField(max_length=100, blank=True, null=True)

    def clean(self):
        if self.account_type == "job_seeker" and not self.skills:
            raise ValidationError("Job Seeker must have skills")
        if self.account_type == "employer" and not self.organization:
            raise ValidationError("Employer must have organization and company website")

    def __str__(self):
        return f"{self.user.username} ({self.account_type})"
