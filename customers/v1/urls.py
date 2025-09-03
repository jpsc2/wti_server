from django.urls import path, include
from customers.v1.views import CustomerList, CustomerUpsert, CustomerDelete

urlpatterns = [
    path('customer_list/', CustomerList.as_view(), name="PROJECT_GET_CUSTOMER_LIST"),
    path('customer_upsert/', CustomerUpsert.as_view(), name="PROJECT_GET_CUSTOMER_LIST"),
    path('customer_delete/', CustomerDelete.as_view(), name="DELETE_CUSTOMER"),
]
