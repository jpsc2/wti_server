from django.db import models
from customers.models import Customer


class Site(models.Model):
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    class Meta(object):
        db_table = "site"
