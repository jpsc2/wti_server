from django.urls import path
from authentication.v1.views import Login, UserData

urlpatterns = [
    path('login/', Login.as_view(), name='AUTHENTICATION_LOGIN_DETAILS'),
    path('user_data/', UserData.as_view(), name='AUTHENTICATION_USER_DETAILS'),
]
