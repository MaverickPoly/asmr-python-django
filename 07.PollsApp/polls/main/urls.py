from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("poll/create/", views.create_poll, name="create_poll"),
    path("poll/<int:poll_id>/solve/", views.solve_poll, name="solve_poll"),
    path("poll/<int:poll_id>/users/", views.poll_users, name="poll_users"),
    path("poll/<int:poll_id>/delete/", views.delete_poll, name="delete_poll"),

    path("profile/", views.profile, name="profile"),

    # Auth
    path("login/", views.login_user, name="login_user"),
    path("logout/", views.logout_user, name="logout_user"),
    path("signup/", views.signup_user, name="signup_user"),
]

