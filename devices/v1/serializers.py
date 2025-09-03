from rest_framework import serializers


class DevicesSerializer(serializers.Serializer):
    id = serializers.IntegerField(default=None)
    name = serializers.CharField(max_length=250)
    mac = serializers.CharField(max_length=250)
    description = serializers.CharField( default=None)
    site_id = serializers.IntegerField()


class GetDevicesSerializer(serializers.Serializer):
    device_id = serializers.CharField()


class AssignDevicesSerializer(serializers.Serializer):
    device_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    remove = serializers.BooleanField()


class AssignSiteSerializer(serializers.Serializer):
    site_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    remove = serializers.BooleanField()


class AssignCustomerSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    remove = serializers.BooleanField()





class DeviceMaintenanceHistoryFeedBackSerializer(serializers.Serializer):
    pass    