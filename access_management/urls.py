from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('v1/', include('access_management.v1.urls')),
]
