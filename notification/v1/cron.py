import datetime
import recurrence
from notification.models import Notification
from django.contrib.auth.models import User
from devices.models import Devices
from authentication.models import (UserCustomerMapping,
                                   UserSiteMapping,
                                   UserDeviceMapping)



pattern = recurrence.Recurrence(include_dtstart=False).between(
    datetime.datetime.now(),
    (datetime.datetime.now()+datetime.timedelta(days=365))
)


class SendMaintenanceRemainder(object):
    
    def __init__(self,device):
        self.device = device
        self.users = self._users()
    
    def _users(self):
        device_mapping = list(UserDeviceMapping.objects.filter(devices__in=[self.device]))
        site_mapping =list(UserSiteMapping.objects.filter(sites__in=[self.device.site]))
        customer_mapping = list(UserCustomerMapping.objects.filter(customers__in=[self.device.site.customer]))
    
        users = []
        for mapping in device_mapping + site_mapping + customer_mapping:
            if mapping.user.email:
                users.append(mapping.user)
        
        return users

    def _create_entry_in_notification(self):
        for user in self.users:
            print(user)
            notification = Notification(
                user=user,
                image="https://cdn-icons-png.flaticon.com/512/1624/1624008.png",
                title=f"Device {self.device.name} Need Maintenance.",
                subtitle=f"Device {self.device.maintenance_date} maintenance date is scheduled for 08/08/2023. Update Check list if done.",
                action='MAINTENANCE_UPCOMMING',
                device=self.device
            )
            notification.save()


    def send_email(self):
        pass
        #TODO:  call email send lambda here

    
    def perform_task_and_get_data(self):
        self._create_entry_in_notification()
        self.send_email()


def send_maintenance_reminder():
    current_datetime = datetime.datetime.now()
    devices = Devices.objects.filter(maintenance_date__gte=current_datetime,maintenance_date__lte = current_datetime+datetime.timedelta(days=30))
    #devices = Devices.objects.all()
    for device in devices:
        SendMaintenanceRemainder(device=device).perform_task_and_get_data()
        print(device.name,device.name)
    
      