from devices.models import Devices
from sites.models import Site
from customers.models import Customer
from authentication.models import UserCustomerMapping, UserSiteMapping, UserDeviceMapping
from authentication.models import User
from common.models import AdministratorEmail


class GetDeviceMailIds(object):
    def __init__(self, device_id):
        self.device_id = device_id
        self.device_data = self.device_model()

    def device_model(self):
        device_data: Devices = Devices.objects.get(mac=self.device_id)
        return device_data

    def device_info(self):
        data = {}
        site: Site = self.device_data.site
        customer: Customer = site.customer
        data = {
            'device_data': {
                'name': self.device_data.name,
                'device_id': self.device_data.device_id,
                'description': self.device_data.description,
            },
            'site_data': {
                'name': site.name,
                'description': site.description,
            },
            'customer_data': {
                'name': customer.name,
                'email_id': customer.email,
                'phone_no': customer.phone_number,
            }
        }
        return data

    def _user_email_ids(self):
        customerMapping = UserCustomerMapping.objects.filter(customers__in=[self.device_data.site.customer])
        sitesMapping = UserSiteMapping.objects.filter(sites__in=[self.device_data.site])
        deviceMapping = UserDeviceMapping.objects.filter(devices__in=[self.device_data])
        users = [x.user for x in customerMapping] + [x.user for x in sitesMapping] + [x.user for x in deviceMapping]
        email_ids = User.objects.filter(id__in=[user.id for user in users]).values(*['email'])
        email_ids =[data['email'] for data in email_ids]
        return email_ids

    def administrator_email_ids(self):
        email_ids = AdministratorEmail.objects.all().values(*['email'])
        email_ids = [data['email'] for data in email_ids]
        return email_ids

    def perform_task(self):
        data = {}
        try:
            data['success'] = True
            data['user_emails'] = self._user_email_ids()
            data['administrator_emails'] = self.administrator_email_ids()
        except Exception as e:
            print("ERROR in GetDeviceMailIds due to : ", str(e))
            data['success'] = False
            data['error'] = str(e)
        return data
