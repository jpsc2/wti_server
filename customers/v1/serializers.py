from rest_framework import serializers
from common.v1.shared.serializers import ListFilterSerializer


class CustomerSerializer(serializers.Serializer):
    id = serializers.IntegerField(default=None)
    name = serializers.CharField(max_length=250)
    email = serializers.EmailField(max_length=250, default=None)
    phone_number = serializers.CharField(max_length=250, default=None)
    description = serializers.CharField(default=None)


class GetCustomerSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
