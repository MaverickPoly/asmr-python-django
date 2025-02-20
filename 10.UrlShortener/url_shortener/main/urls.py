from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="home"),
    path("url/<path:path>", views.view, name="view"),
]
