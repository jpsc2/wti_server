from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from devices.v1.service import device_service
from devices.v1.serializers import (DevicesSerializer, GetDevicesSerializer,AssignDevicesSerializer,AssignCustomerSerializer,AssignSiteSerializer)
from common.v1.shared.serializers import ListFilterSerializer
from sites.v1.service import site_service
from devices.v1.service import device_details_service

class DevicesList(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = ListFilterSerializer(data=request.data)
        if serializer.is_valid():

            serializer_data = serializer.validated_data
            print("serializer_data", serializer_data)
            data = device_service.DevicesListService(user=user, customer_ids=serializer_data[
                'customer_ids'], site_ids=serializer_data['site_ids'], user_ids=serializer_data['user_ids'],
                                                     all=serializer_data['all']).perform_task_and_get_data()
        else:
            data = serializer.errors
        return Response(data=data)

    def post(self, request):
        return self.get(request)


class DeviceUpsert(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = GetDevicesSerializer(data=request.data)
        if serializer.is_valid():
            serializer_data = serializer.validated_data
            user = request.user
            data = site_service.DevicesListService(user=user, device_ids=[serializer_data['device_id']],
                                                   all=serializer_data['all']).perform_task_and_get_data()
        else:
            data = serializer.errors
        return Response(data=data)

    def post(self, request):
        serializer = DevicesSerializer(data=request.data)
        if serializer.is_valid():
            serializer_data = serializer.validated_data
            data = device_service.DeviceUpsert(**serializer_data).upsert()
        else:
            data = serializer.errors
        return Response(data=data)


class DeviceDelete(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GetDevicesSerializer(data=request.data)
        if serializer.is_valid():
            serializer_data = serializer.validated_data
            data = device_service.DeviceDelete(**serializer_data).delete()
        else:
            data = serializer.errors
        return Response(data=data)


class AssignDevice(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AssignDevicesSerializer(data=request.data)
        if serializer.is_valid():
            serializer_data = serializer.validated_data
            print('serializer_data',serializer_data)
            data = device_service.AssignDevice(**serializer_data).perfrom()
        else:
            data = serializer.errors
        return Response(data=data)


class DeviceEmails(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GetDevicesSerializer(data=request.data)
        if serializer.is_valid():
            serializer_data = serializer.validated_data
            print('serializer_data', serializer_data)
            data = device_details_service.GetDeviceMailIds(**serializer_data).perform_task()
        else:
            data = serializer.errors
        return Response(data=data)


