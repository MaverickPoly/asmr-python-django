from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.home, name="home"),

    # Utils
    path("event/<int:id>/register/", views.event_register, name="event_register"),
    path("event/<int:id>/delete/", views.event_delete, name="event_delete"),

    # Categories
    path("categories/", views.categories, name="categories"),
    path("category/create/", views.create_category, name="create_category"),
    path("category/<int:id>/events/", views.category_events, name="category_events"),
    path("category/<int:id>/delete/", views.category_delete, name="category_delete"),
    path("category/<int:id>/update/", views.category_update, name="category_update"),

    # Events
    path("event/create/", views.create_event, name="create_event"),
    path("event/<int:id>/details/", views.event_details, name="event_details"),
    path("event/<int:id>/update/", views.event_update, name="event_update"),
    path("event/<int:id>/payment/", views.event_payment, name="event_payment"),
    path("event/<int:id>/comments/", views.event_comments, name="event_comments"),

    # Search
    path("search/", views.search, name="search"),
    path("filter/<str:query>/", views.filter, name="filter"),

    # Profile
    path("profile/<int:user_id>/", views.profile, name="profile"),
    path("profile/<int:user_id>/", views.profile, name="profile"),

    # Auth
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
