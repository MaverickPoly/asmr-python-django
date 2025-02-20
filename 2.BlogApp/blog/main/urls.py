from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.index, name="home"),
    path("create_post/", views.create_blog, name="create_blog"),
    path("post/<int:post_id>/", views.post_details, name="blog_details"),
    path("post/<int:post_id>/edit/", views.edit_post, name="edit_post"),
    path("post/<int:post_id>/delete/", views.delete_post, name="delete_post"),

    # Utils
    path("post/<int:post_id>/like/", views.like_post, name="like_post"),  # Like & Unlike post(toggle)
    path("profile/<int:user_id>/follow/", views.follow_unfollow, name="follow_unfollow"),  # Follow & Unfollow user

    # General
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("profile/<int:user_id>/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/<int:user_id>/followers/", views.user_followers, name="user_followers"),

    # Authentication
    path("auth/login/", views.login_user, name="login"),
    path("auth/logout/", views.logout_user, name="logout"),
    path("auth/signup/", views.signup_user, name="signup"),
    path("auth/change_password/", views.change_password, name="change_password"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
