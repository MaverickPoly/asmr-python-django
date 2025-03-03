from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="home"),

    # Auth
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("signup/", views.signup_user, name="signup"),
    path("auth/github/", views.github_auth, name="github_auth"),
]
