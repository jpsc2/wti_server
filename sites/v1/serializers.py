from rest_framework import serializers

class SiteSerializer(serializers.Serializer):
    id = serializers.IntegerField(default=None)
    name = serializers.CharField(max_length=250)
    description = serializers.CharField( default=None)
    customer_id = serializers.IntegerField()


class GetSiteSerializer(serializers.Serializer):
    site_id = serializers.IntegerField()
