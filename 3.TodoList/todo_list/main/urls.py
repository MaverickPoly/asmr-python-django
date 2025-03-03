from django.urls import path
from . import views

urlpatterns = [
    # Todos
    path("", views.index, name="home"),
    path("create/", views.create, name="create"),
    path("delete/", views.delete, name="delete"),
    path("update/<int:todo_id>/", views.update, name="update"),
    path("toggle_complete/", views.toggle_complete, name="toggle"),   # Toggle Completed
    path("profile/", views.profile, name="profile"),
    path("todo/<int:todo_id>/", views.todo_details, name="todo_details"),

    # Auth
    path("login/", views.login_user, name="login"),
    path("register/", views.register_user, name="register"),
    path("logout/", views.logout_user, name="logout"),
]
