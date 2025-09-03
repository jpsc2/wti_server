from django.urls import path, include
from access_management.v1.views import UserList, UserUpsert, UserDelete

urlpatterns = [
    path('user_list/', UserList.as_view(), name="PROJECT_GET_DEVICES_LIST"),
    path('user_delete/', UserDelete.as_view(), name="USER_DELETE"),
    path('user_upsert/', UserUpsert.as_view(), name="USER_UPSERT"),

]
