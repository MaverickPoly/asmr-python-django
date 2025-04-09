from django.urls import path
from . import views


urlpatterns = [
    path("profile/<int:user_id>/", views.profile_view, name="profile_view"),
    path("profile/", views.current_profile, name="current_profile"),
    path("profile/edit/", views.edit_profile_view, name="edit_profile_view"),
]