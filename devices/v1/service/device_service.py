from authentication.models import User, UserCustomerMapping, UserSiteMapping, UserDeviceMapping
from sites.models import Site
from devices.models import Devices
from customers.models import Customer


class DevicesListService(object):
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

        site_mapping = []
        try:
            site_mapping = UserSiteMapping.objects.filter(user=self.user, sites__in=Site.objects.filter(
                id__in=self.site_ids))
        except Exception as e:
            print('Error on SiteListService.site_mapping', e)

        device_ids = []

        if site_mapping:
            try:
                device_ids.extend(
                    list(Devices.objects.filter(site_id__in=self.site_ids).values_list('id', flat=True)))
            except Exception as e:
                print('Error on SiteListService.perform_task_and_get_data', e)
        else:
            try:
                device_ids.extend(
                    list(Devices.objects.filter(site_id__in=self.site_ids, id__in=[x for x in
                                                                                   UserDeviceMapping.objects.filter(
                                                                                       user=self.user).values_list(
                                                                                       'devices',
                                                                                       flat=True)]).values_list(
                        'id', flat=True)))
            except Exception as e:
                print('Error on SiteListService.perform_task_and_get_data', e)

        customer_mapping = []
        try:
            customer_mapping = UserCustomerMapping.objects.filter(user=self.user, customers__in=Customer.objects.filter(
                id__in=self.customer_ids))
        except Exception as e:
            print('Error on SiteListService.perform_task_and_get_data', e)

        if customer_mapping:
            try:
                device_list = Devices.objects.all()
                for device in device_list:
                    if device.site.id in self.site_ids and device.site.customer.id in self.customer_ids:
                        device_ids.append(device.id)
            except Exception as e:
                print('Error in SiteListService.device_list', e)

        print('device_ids', device_ids)
        devices_objects = Devices.objects.filter(id__in=device_ids)
        if not devices_objects:
            devices_objects = []
        return devices_objects

    def perform_task_and_get_data(self):
        devices_list = list()

        devices_objects = self._get_user_specific_device()
        if devices_objects:
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


class DeviceUpsert(object):

    def __init__(self, id, name, description, mac, site_id):
        self.id = id
        self.name = name
        self.description = description
        self.mac = mac
        self.site_id = site_id
        self.response = self._init_response()

    @staticmethod
    def _init_response():
        return {
            'success': False,
            'error': 'Server Error',
            'message': '',
        }

    def _update_device_model(self):
        try:
            device_object = Devices.objects.get(id=self.id)
            if self.name:
                device_object.name = self.name
            if self.site_id:
                device_object.customer_id = self.site_id
            if self.mac:
                device_object.mac = self.mac
            if self.description:
                device_object.description = self.description
            device_object.save()
            self.response['success'] = True
            self.response['message'] = 'user is updated successfully.'
        except Exception as e:
            print('Error on DeviceUpsert._update_device_model due to ', e)
            self.response['error'] = str(e)

    def _create_device_object(self):
        try:
            device_object = Devices.objects.create(
                name=self.name,
                description=self.description,
                site_id=self.site_id,
                mac=self.mac
            )
            self.response['success'] = True
            self.response['message'] = 'Device is created successfully.'
        except Exception as e:
            print('Error on DeviceUpsert._create_device_object due to ', e)
            self.response['error'] = str(e)

    def upsert(self):
        if self.id:
            self._update_device_model()
        else:
            self._create_device_object()
        return self.response


class DeviceDelete(object):

    def __init__(self, device_id):
        self.device_id = device_id
        self.response = self._init_response()

    @staticmethod
    def _init_response():
        return {
            'success': False,
            'error': 'Server Error',
            'message': '',
        }

    def delete(self):
        try:
            print("id", self.device_id)
            device_object: User = Devices.objects.get(id=self.device_id)
            device_object.delete()
            self.response['success'] = True
            self.response['message'] = 'device is deleted successfully.'
        except Exception as e:
            print('device on DeviceDelete._update_user_model due to ', e)
            self.response['error'] = str(e)
        return self.response


class AssignDevice(object):

    def __init__(self, user_id, device_id, remove=False):
        self.user_id = user_id
        self.device_id = device_id
        self.remove = remove
        self.response = self._init_response()

    @staticmethod
    def _init_response():
        return {
            'success': False,
            'error': 'Server Error',
            'message': '',
        }

    def perfrom(self):
        try:
            try:
                user_device_mapping = UserDeviceMapping.objects.get(user_id=self.user_id)
            except Exception as e:
                user_device_mapping = UserDeviceMapping.objects.create(user_id=self.user_id)
            if self.remove:
                user_device_mapping.devices.remove(Devices.objects.get(id=self.device_id))
            else:
                user_device_mapping.devices.add(Devices.objects.get(id=self.device_id))
            user_device_mapping.save()
            self.response['success'] = True
            self.response['message'] = 'device access updated successfully.'
        except Exception as e:
            print('device on DeviceDelete._update_user_model due to ', e)
            self.response['error'] = str(e)
        return self.response


class AssignSite(object):

    def __init__(self, user_id, site_id, remove=False):
        self.user_id = user_id
        self.site_id = site_id
        self.remove = remove,
        self.response = self._init_response()

    @staticmethod
    def _init_response():
        return {
            'success': False,
            'error': 'Server Error',
            'message': '',
        }

    def perfrom(self):
        try:
            user_site_mapping = UserSiteMapping.objects.get(user_id=self.user_id)
            if self.remove:
                user_site_mapping.sites.remove(Site.objects.get(id=self.site_id))
            else:
                user_site_mapping.sites.add(Site.objects.get(id=self.site_id))
            user_site_mapping.save()
            self.response['success'] = True
            self.response['message'] = 'site is assigned successfully.'
        except Exception as e:
            print('device on DeviceDelete._update_user_model due to ', e)
            self.response['error'] = str(e)
        return self.response


class AssignCustomer(object):
    def __init__(self, user_id, customer_id, remove):
        self.user_id = user_id
        self.customer_id = customer_id
        self.remove = remove
        self.response = self._init_response()

    @staticmethod
    def _init_response():
        return {
            'success': False,
            'error': 'Server Error',
            'message': '',
        }

    def perfrom(self):
        try:
            user_customer_mapping = UserCustomerMapping.objects.get(user_id=self.user_id)
            user_customer_mapping.devices.add(Customer.objects.get(id=self.customer_id))
            if self.remove:
                user_customer_mapping.customers.remove(Customer.objects.get(id=self.customer_id))
            else:
                user_customer_mapping.customers.add(Customer.objects.get(id=self.customer_id))
            user_customer_mapping.save()
            self.response['success'] = True
            self.response['message'] = 'site is assigned successfully.'
        except Exception as e:
            print('device on DeviceDelete._update_user_model due to ', e)
            self.response['error'] = str(e)
        return self.response
