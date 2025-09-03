from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication , SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from notification.v1.serializers import SendNotificationSerializer,SaveFCMTokenSerializer
from notification.v1.services import notification_list_service, push_notification_service, device_token_manager



class NotificationList(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = notification_list_service.NotificationList(user=request.user).perform_task_and_get_data()
        return Response(data=data)

    def post(self, request):
        return self.get(request)
    
class SendNotification(APIView):

    def post(self, request):
        serializer = SendNotificationSerializer(data=request.data)
        if serializer.is_valid():
            data = push_notification_service.SendPushNotification(**serializer.validated_data).perform_task()
        else:
            data = serializer.errors
        return Response(data=data)
    

class SaveFCMToken(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SaveFCMTokenSerializer(data=request.data)
        if serializer.is_valid():
            data = device_token_manager.DeviceTokenManager(user=request.user,token=serializer.validated_data['token']).perform_task()
        else:
            data = serializer.errors
        return Response(data=data)