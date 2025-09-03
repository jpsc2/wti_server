from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('v1/', include('devices.v1.urls')),
]
