from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication , SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from access_management.v1.service import user_service
from access_management.v1.serializers import GetUsererializer, UserSerializer


class UserList(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = user_service.UserListService(user=user).perform_task_and_get_data()
        return Response(data=data)

    def post(self, request):
        return self.get(request)


class UserUpsert(APIView):

    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer_data = serializer.validated_data
            data = user_service.UserUpsert(**serializer_data).upsert()
        else:
            data = serializer.errors
        return Response(data=data)


class UserDelete(APIView):

    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GetUsererializer(data=request.data)
        if serializer.is_valid():
            serializer_data = serializer.validated_data
            data = user_service.UserDelete(**serializer_data).delete()
        else:
            data = serializer.errors
        return Response(data=data)