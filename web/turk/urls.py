"""turk URL Configuration."""
from django.contrib import admin
from django.urls import include, path

from turk.api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
    path('', include('social_django.urls', namespace='social')),
]
