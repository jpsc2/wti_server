
from django.urls import path, include
from report.v1.views import ReportView,ReportDevicesList

urlpatterns = [
    path('report/', ReportView.as_view(), name="PROJECT_GET_DEVICES_LIST"),
    path('report_device_list/', ReportDevicesList.as_view(), name="PROJECT_GET_DEVICES_LIST"),

]



