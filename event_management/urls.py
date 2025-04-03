from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Import Django's auth views
from django.conf import settings
from django.conf.urls.static import static  # Import static file handling

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # Login route
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout route
    path('', include('events.urls')),  # Include events app URLs
]

# Serve media files (event banners) in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
