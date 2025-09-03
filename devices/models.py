from django.db import models
from sites.models import Site
from recurrence.fields import RecurrenceField
# Create your models here.


class Devices(models.Model):
    name = models.CharField(max_length=250, unique=True)
    mac = models.CharField(max_length=250, unique=True)
    description = models.TextField(null=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.DO_NOTHING)
    latitude = models.CharField(max_length=250, null=True,blank=True,default='')
    longitude = models.CharField(max_length=250, null=True,blank=True,default='')
    maintenance_date = models.DateField(default='',null=True,blank=True)
    maintenance = RecurrenceField(default='', null=True, blank=True)

    def __str__(self):
        return self.name + " , " + self.mac

    class Meta(object):
        db_table = "device"


class DeviceMaintenanceHistory(models.Model):
    device = models.ForeignKey(Devices, on_delete=models.DO_NOTHING)
    remark = models.TextField(null=True,default='',blank=True)
    date = models.DateField(auto_now=True,null=True,blank=True)
    month_year = models.CharField(max_length=500,null=True,default='',blank=True)
    rating = models.CharField(max_length=50,null=True,default='',blank=True)
    supervisor = models.CharField(max_length=500,null=True,default='',blank=True)
    operator = models.CharField(max_length=500,null=True,default='',blank=True)
    sr_no = models.IntegerField(null=True,default=None,blank=True)
    checked_by = models.CharField(max_length=500,null=True,default='',blank=True)
    verified_by = models.CharField(max_length=500,null=True,default='',blank=True)
    check_1 = models.BooleanField(name='Clean the surrounding area of the job',db_column='check_1',null=True,default='',blank=True)
    check_2 = models.BooleanField(name='Check incoming supply voltage, current and keep the record',db_column='check_2',null=True,default='',blank=True)
    check_3 = models.BooleanField(name='Check outgoing supply voltage and current and keep the record',db_column='check_3',null=True,default='',blank=True)
    check_4 = models.BooleanField(name='Check the winding and core temperature reading on WTI relay and keep the record',db_column='check_4',null=True,default='',blank=True)
    check_5 = models.BooleanField(name='Check RMU manometer gas reading. It should be in the green zone',db_column='check_5',null=True,default='',blank=True)
    check_6 = models.BooleanField(name='Check proper supply for control and protection circuit',db_column='check_6',null=True,default='',blank=True)
    check_7 = models.BooleanField(name='Check the display of RMU protection relay',db_column='check_7',null=True,default='',blank=True)
    check_8 = models.BooleanField(name='Check for any abnormal noise from the transformer. YES/NO',db_column='check_8',null=True,default='',blank=True)
    check_9 = models.BooleanField(name='Check fire extinguisher expiry date details.',db_column='check_9',null=True,default='',blank=True)


