from django.db import models
from customers.models import Customer
from devices.models import Devices
from sites.models import Site
from django.contrib.auth.models import User


class UserCustomerMapping(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    customers = models.ManyToManyField(Customer, blank=True)

    class Meta(object):
        db_table = 'user_customer_mapping'

    def __str__(self):
        return self.user.__str__()


class UserSiteMapping(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    sites = models.ManyToManyField(Site, blank=True)

    class Meta(object):
        db_table = 'user_site_mapping'

    def __str__(self):
        return self.user.__str__()


class UserDeviceMapping(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    devices = models.ManyToManyField(Devices, blank=True)

    class Meta(object):
        db_table = 'user_device_mapping'

    def __str__(self):
        return self.user.__str__()