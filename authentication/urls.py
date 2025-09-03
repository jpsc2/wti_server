from django.urls import path, include

urlpatterns = [
    path('v1/', include('authentication.v1.urls')),
]
