from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(default=None)
    name = serializers.CharField(max_length=250, allow_blank=True)
    username = serializers.CharField(max_length=250, allow_blank=True)
    is_admin = serializers.BooleanField(default=False)
    password = serializers.CharField(default=False, allow_blank=True)


class GetUsererializer(serializers.Serializer):
    user_id = serializers.IntegerField()



