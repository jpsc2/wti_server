import boto3
from boto3.dynamodb.conditions import Key
from datetime import date, timedelta
import csv

from django.contrib.auth.models import User

from authentication.models import UserCustomerMapping, UserSiteMapping, UserDeviceMapping
from devices.models import Devices
from sites.models import Site


class GetDeviceReport(object):
    TABLE_NAME = 'dynamodb'
    REGION_NAME = 'us-east-1'

    def __init__(self, device_id, start_date, end_date):
        self.device_id = device_id
        self.start_date = start_date
        self.end_date = end_date

    def _dynamo_table(self):
        dynamo_client = boto3.resource(self.TABLE_NAME, region_name=self.REGION_NAME)
        dynamo_table = dynamo_client.Table('dtele2'|'dtele3'|'dtele4')
        return dynamo_table

    def daterange(self, start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    def _date_list(self):
        date_list = []
        for single_date in self.daterange(self.start_date, self.end_date):
            single_date:date = single_date
            date_str = str(single_date.day)+"-"+str(single_date.month) + "-" + str(single_date.year)[-2:]
            date_list.append(date_str)
        return date_list

    def _device_data(self):
        date_list = self._date_list()
        device_data_list = []
        dynamo_table = self._dynamo_table()
        for ddate in date_list:
            print('ddate', ddate)
            device_data = dynamo_table.query(
                KeyConditionExpression=Key('d_id').eq(self.device_id) & (Key('timestamp').begins_with(ddate))
            )
            device_data_list.extend(device_data['Items'])
        return device_data_list

    def perform_task(self):
        try:
            self._date_list()
            data = self._device_data()
            return {'success': True, 'data': data, 'error': None}
        except Exception as e:
            print("ERROR IN GetDeviceReport.perform_task due to ", e)
            return {'success': False, 'data': {}, 'error': str(e)}


class DevicesListReForReportService(object):
    def __init__(self, user: User, customer_ids=None, site_ids=None, device_ids=None, all=False, user_ids=[]):
        self.user: User = user
        self.customer_ids = customer_ids
        self.site_ids = site_ids
        self.device_ids = device_ids
        self.all = all
        self.user_ids = user_ids

    def _customer_ids(self):
        try:
            self.customer_ids = UserCustomerMapping.objects.get(user=self.user).customers.all().values_list('id',
                                                                                                            flat=True)
        except Exception as e:
            print('Error in DevicesListService._customer_list', e)

    def _site_ids(self):
        if not self.customer_ids:
            self._customer_ids()
        self.site_ids = Site.objects.filter(customer_id__in=self.customer_ids).values_list('id', flat=True)

    def _get_user_specific_device(self):
        try:
            customer_ids = list(
                UserCustomerMapping.objects.get(user=self.user).customers.all().values_list('id', flat=True))
        except Exception as e:
            print('Error on DevicesListService._get_user_specific_device', e)
            customer_ids = []
        try:
            site_ids = list(
                UserSiteMapping.objects.get(user_id__in=self.user_ids).sites.all().values_list('id', flat=True))
        except Exception as e:
            print('Error on DevicesListService._get_user_specific_device', e)
            site_ids = []
        try:
            site_ids.extend(list(Site.objects.filter(customer_id__in=customer_ids).values_list('id', flat=True)))
        except Exception as e:
            print('Error on DevicesListService._get_user_specific_device', e)
        try:
            device_ids = list(
                UserDeviceMapping.objects.get(user=self.user).devices.all().values_list('id', flat=True))
        except Exception as e:
            device_ids = []
            print('Error on DevicesListService._get_user_specific_device', e)
        try:
            device_ids.extend(list(Devices.objects.filter(site_id__in=site_ids).values_list('id', flat=True)))
        except Exception as e:
            print('Error on DevicesListService._get_user_specific_device', e)
        print('device_ids', device_ids)
        devices_objects = Devices.objects.filter(id__in=device_ids)
        return devices_objects

    def perform_task_and_get_data(self):
        devices_list = list()

        devices_objects = self._get_user_specific_device()

        for devices_object in devices_objects:
            devices_object: Devices = devices_object
            project = {
                "id": devices_object.id,
                "name": devices_object.name,
                "mac": devices_object.mac,
                "description": devices_object.description,
                "maintenance_date":devices_object.maintenance_date,
                "latitude":devices_object.latitude,
                "longitude":devices_object.longitude,
            }
            devices_list.append(project)
        return devices_list
