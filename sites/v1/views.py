from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication , SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from sites.v1.service import ( site_service)
from sites.v1.serializers import (SiteSerializer,GetSiteSerializer)
from common.v1.shared.serializers import ListFilterSerializer


class SitetList(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = ListFilterSerializer(data=request.data)
        if serializer.is_valid():
            serializer_data = serializer.validated_data
            data = site_service.SiteListService(user=user, customer_ids=serializer_data[
                'customer_ids'], attach_sub_item=serializer_data['attach_sub_item']).perform_task_and_get_data()
        else:
            data = serializer.errors
        return Response(data=data)

    def post(self, request):
        return self.get(request)


class SiteUpsert(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = GetSiteSerializer(data=request.data)
        if serializer.is_valid():
            serializer_data = serializer.validated_data
            user = request.user
            data = site_service.SiteListService(user=user).perform_task_and_get_data()
        else:
            data = serializer.errors
        return Response(data=data)

    def post(self, request):
        serializer = SiteSerializer(data=request.data)
        if serializer.is_valid():
            serializer_data = serializer.validated_data
            data = site_service.SiteUpsert(**serializer_data).upsert()
        else:
            data = serializer.errors
        return Response(data=data)


class SiteDelete(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GetSiteSerializer(data=request.data)
        if serializer.is_valid():
            serializer_data = serializer.validated_data
            data = site_service.SiteDelete(**serializer_data).delete()
        else:
            data = serializer.errors
        return Response(data=data)