from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="home"),
    path("create/", views.create, name="create"),
    path("profile/", views.profile, name="profile"),
    path("quote/<int:quote_id>", views.read_quote, name="read_quote"),
    path("toggle_favourite/<int:quote_id>", views.toggle_favourite, name="toggle_favourite"),

    # Auth
    path("login/", views.login_user, name="login"),
    path("register/", views.register_user, name="register"),
    path("logout/", views.logout_user, name="logout"),
]
