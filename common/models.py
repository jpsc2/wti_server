from django.db import models


# Create your models here.


class AdministratorEmail(models.Model):
    email = models.EmailField()
    description = models.TextField(default='', null=True)

    class Meta(object):
        db_table = 'administrator_email'

