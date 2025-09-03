from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from devices.v1.serializers import GetDevicesSerializer
from report.v1.services import get_device_report


class ReportSerializer(serializers.Serializer):
    device_id = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()





