from django.http import HttpResponse
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.v1.shared.serializers import ListFilterSerializer
from report.v1.serializers import ReportSerializer
from report.v1.services import get_device_report
import csv


class ReportView(APIView):
    # authentication_classes = [TokenAuthentication, SessionAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = request.GET if request.method == 'GET' else request.data  #  This line is key!
        serializer = ReportSerializer(data=data)
        if serializer.is_valid():
            serializer_data = serializer.validated_data
            print("serializer_data", serializer_data)
            data = get_device_report.GetDeviceReport(**serializer_data).perform_task()
            response = HttpResponse(
                content_type='text/csv',
                headers={'Content-Disposition': 'attachment; filename="report.csv"'},
            )
            writer = csv.writer(response)
            if data['data']:
                writer.writerow(data['data'][0].keys())
                for row in data['data']:
                    writer.writerow(row.values())
            return response
        else:
            return Response(data=serializer.errors, status=400)  #  Proper error status

    def post(self, request):
        return self.get(request)

class ReportDevicesList(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = ListFilterSerializer(data=request.data)
        if serializer.is_valid():

            serializer_data = serializer.validated_data
            print("serializer_data", serializer_data)
            data = get_device_report.DevicesListReForReportService(user=user, customer_ids=serializer_data[
                'customer_ids'], site_ids=serializer_data['site_ids'], user_ids=serializer_data['user_ids'],
                                                                   all=serializer_data[
                                                                       'all']).perform_task_and_get_data()
        else:
            data = serializer.errors
        return Response(data=data)

    def post(self, request):
        return self.get(request)
