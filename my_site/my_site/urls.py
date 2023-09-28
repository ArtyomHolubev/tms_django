from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('my_app/', include('my_app.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('drf_app/', include('drf_app.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path("debug/", include("debug_toolbar.urls")),
]
