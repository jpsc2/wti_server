
from rest_framework import serializers

class SendNotificationSerializer(serializers.Serializer):
    device_id = serializers.CharField()
    message = serializers.CharField()
    flag = serializers.IntegerField()


class SaveFCMTokenSerializer(serializers.Serializer):
    token = serializers.CharField()
