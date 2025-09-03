from django.urls import path, include
from devices.v1.views import DevicesList, DeviceUpsert, DeviceDelete, AssignDevice, DeviceEmails


urlpatterns = [
    path('devices_list/', DevicesList.as_view(), name="PROJECT_GET_DEVICES_LIST"),
    path('devices_upsert/', DeviceUpsert.as_view(), name="DEVICE_UPSERT"),
    path('device_delete/', DeviceDelete.as_view(), name="DELETE_DEVICE"),
    path('assign_device/', AssignDevice.as_view(), name="DELETE_DEVICE"),
    path('device_emails/', DeviceEmails.as_view(), name="DELETE_DEVICE"),
]
