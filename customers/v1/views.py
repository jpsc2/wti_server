from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from customers.v1.service import customer_service
from customers.v1.serializers import (ListFilterSerializer, CustomerSerializer, GetCustomerSerializer)
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers


class CustomerList(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(vary_on_headers('Authorization', 'Cookie'), name='dispatch')
    @method_decorator(cache_page(120), name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        user = request.user
        serializer = ListFilterSerializer(data=request.query_params)  # use query_params
        if serializer.is_valid():
            serializer_data = serializer.validated_data
            data = customer_service.CustomerListService(
                user=user,
                attach_sub_item=serializer_data.get('attach_sub_item', False)
            ).perform_task_and_get_data()
        else:
            data = serializer.errors
        return Response(data=data)

    def post(self, request):
        serializer = ListFilterSerializer(data=request.data)
        if serializer.is_valid():
            serializer_data = serializer.validated_data
            data = customer_service.CustomerListService(
                user=request.user,
                attach_sub_item=serializer_data.get('attach_sub_item', False)
            ).perform_task_and_get_data()
        else:
            data = serializer.errors
        return Response(data=data)


class CustomerUpsert(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = GetCustomerSerializer(data=request.query_params)  # use query_params
        if serializer.is_valid():
            serializer_data = serializer.validated_data
            user = request.user
            data = customer_service.CustomerListService(user=user).perform_task_and_get_data()
        else:
            data = serializer.errors
        return Response(data=data)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer_data = serializer.validated_data
            data = customer_service.CustomerUpsert(user=request.user, **serializer_data).upsert()
        else:
            data = serializer.errors
        return Response(data=data)


class CustomerDelete(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GetCustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer_data = serializer.validated_data
            data = customer_service.CustomerDelete(**serializer_data).delete()
        else:
            data = serializer.errors
        return Response(data=data)
