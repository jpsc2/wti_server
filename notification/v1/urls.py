from django.urls import path
from notification.v1.views import NotificationList, SendNotification, SaveFCMToken

urlpatterns = [
    path('notification_list/', NotificationList.as_view(), name="NotificationList"),
    path('send_notification/', SendNotification.as_view(), name="SendNotification"),
     path('save_token/', SaveFCMToken.as_view(), name="SendNotification"),
]
