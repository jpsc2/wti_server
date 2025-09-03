from rest_framework import serializers


class ListFilterSerializer(serializers.Serializer):
    attach_sub_item = serializers.BooleanField(default=False)
    all = serializers.BooleanField(default=False)
    customer_ids = serializers.ListField(child=serializers.IntegerField(), default=None)
    user_ids = serializers.ListField(child=serializers.IntegerField(), default=None)
    site_ids = serializers.ListField(child=serializers.IntegerField(), default=None)
