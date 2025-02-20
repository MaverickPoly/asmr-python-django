from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.index, name="home"),
    path("about/", views.about, name="about"),
    path("profile/<int:profile_id>", views.profile, name="profile"),
    path("book/<int:book_id>", views.book_detail, name="book_detail"),
    path("book/comments/<int:book_id>", views.comments, name="book_comments"),
    path("create_book/", views.create_book, name="create_book"),
    path("update_book/", views.update_book, name="update_book"),
    path("delete_book/", views.delete_book, name="delete_book"),
    path("search_book/", views.search_book, name="search_book"),
    path("tag/<slug:tag>", views.filter_tag, name="tag"),

    # Return & Borrow
    path("borrow_book/", views.borrow_book, name="borrow_book"),
    path("return_book/", views.return_book, name="return_book"),

    # AUTH
    path("login/", views.login_user, name="login"),
    path("register/", views.register_user, name="register"),
    path("logout/", views.logout_user, name="logout"),
    path("change_password/", views.change_password, name="change_password"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

