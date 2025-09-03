from django.db.models.signals import post_save
from django.dispatch import receiver
from devices.models import DeviceMaintenanceHistory,Devices
from notification.models import Notification
import datetime


@receiver(post_save, sender=DeviceMaintenanceHistory)
def update_next_occurrence(sender, instance:DeviceMaintenanceHistory,created, **kwargs):
    if created:
        instance.device.maintenance_date =  instance.device.maintenance.after(datetime.datetime.combine(instance.device.maintenance_date,datetime.datetime.max.time()))
        instance.device.save()
        Notification.objects.filter(device=instance.device).delete()