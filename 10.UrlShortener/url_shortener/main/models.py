from django.db import models


class UrlPath(models.Model):
    path = models.CharField(max_length=300)
    redirect_url = models.URLField()

    def __str__(self):
        return f"{self.path}: {self.redirect_url}"
