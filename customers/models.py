from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=250, unique=True)
    email = models.EmailField(max_length=250, null=True, blank=True)
    phone_number = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta(object):
        db_table = "customer"