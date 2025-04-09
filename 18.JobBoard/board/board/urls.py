from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path("", include("core.urls")),  # Core
    path("accounts/", include("accounts.urls")),  # Accounts
    path("job/", include("job.urls")),  # Job
    path("notifications/", include("notifications.urls")),  # Notifications
    path("user/", include("user.urls")),  # User
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
