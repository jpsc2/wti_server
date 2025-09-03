from django.db import models
from django.contrib.auth.models import User
from devices.models import Devices
# Create your models here.

NOTIFICATION_CHOICES = (('MAINTENANCE_UPCOMMING','MAINTENANCE_UPCOMMING'),('MAINTENANCE_DUE','MAINTENANCE_DUE'),('MAINTENANCE_DONE','MAINTENANCE_DONE'),('OTHER','OTHER'),('CRITICAL_FAILURE','CRITICAL_FAILURE'))

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    image = models.TextField(max_length=250, default='')
    title = models.CharField(max_length=250, default='')
    subtitle = models.TextField(null=True, blank=True,default='')
    action =  models.CharField(max_length=250, default='',choices=NOTIFICATION_CHOICES)
    device = models.ForeignKey(Devices,on_delete=models.DO_NOTHING, null=True, blank=True, default='')
    create_at =models.DateTimeField(auto_now=True,null=True,blank=True)
