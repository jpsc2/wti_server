from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.v1.serializers import LoginSerializers
from authentication.v1.services.user_data_service import UserDataService


class Login(APIView):
    def post(self, request):
        serializer = LoginSerializers(data=request.data)
        if serializer.is_valid():
            return Response(data=serializer.perform_tasks_and_get_data())
        return Response(data=serializer.errors)


class UserData(APIView):

    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(data=UserDataService(user=user).perform_task_get_data())

    def post(self, request):
        return self.get(request)
