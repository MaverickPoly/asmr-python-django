from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="images/profile_images/", null=False)
    bio = models.TextField(max_length=1000)
    city = models.CharField(max_length=100)
    followers = models.ManyToManyField(User, blank=True, related_name="following")

    def __str__(self):
        return self.user.username

    def follow(self, user):
        self.followers.add(user)

    def unfollow(self, user):
        self.followers.remove(user)

    def is_following(self, user):
        return self.followers.filter(id=user.id).exists()


class Post(models.Model):
    author = models.ForeignKey(Profile, related_name="posts", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="images/posts/", null=False)
    likes = models.ManyToManyField(Profile, related_name="liked_posts")

    def __str__(self):
        return self.title
