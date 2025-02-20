from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static


urlpatterns = [
    path("", views.home, name="home"),
    path("cart/", views.cart, name="cart"),
    path("about/", views.about, name="about"),
    path("profile/", views.profile, name="profile"),
    path("create-product/", views.create_product, name="create_product"),
    path("product/<int:product_id>/", views.product_details, name="product_details"),
    path("product/delete", views.delete_product, name="delete_product"),


    # Javascript API
    path("add_to_cart/", views.add_to_cart, name="add_to_cart"),
    path("remove_from_cart/", views.remove_from_cart, name="remove_from_cart"),

    # Auth
    path("login/", views.login_user, name="login"),
    path("register/", views.register_user, name="register"),
    path("logout/", views.logout_user, name="logout")
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
