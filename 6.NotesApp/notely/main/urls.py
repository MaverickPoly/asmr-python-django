from django.urls import path
from . import views


urlpatterns = [
    # Basic
    path("", views.index, name="home"),
    path("profile/", views.profile, name="profile"),
    path("create/", views.create, name="create"),
    path("delete_note/", views.delete_note, name="delete_note"),
    path("update_note/<int:note_id>/", views.update_note, name="update_note"),
    path("note/<int:note_id>/", views.note_details, name="note_details"),
    path("clear-notes/", views.clear_notes, name="clear_notes"),

    # Auth
    path("login/", views.login_user, name="login"),
    path("register/", views.register_user, name="register"),
    path("logout/", views.logout_user, name="logout"),
]
