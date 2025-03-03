from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.index, name="home"),
    path("create/", views.create, name="create"),
    path("quiz/<int:id>/", views.practice_quiz, name="practice-quiz"),
    path("quiz/<int:quiz_id>/result/", views.quiz_result, name="quiz-result"),

    # General
    path("about/", views.about, name="about"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),

    # Auth
    path("login/", views.login_user, name="login"),
    path("register/", views.register_user, name="register"),
    path("logout/", views.logout_user, name="logout"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

