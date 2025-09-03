from django.contrib import admin
from customers.models import Customer
from sites.models import Site
from devices.models import Devices


class SiteInline(admin.TabularInline):
    model = Site


class DevicesInline(admin.TabularInline):
    model = Devices


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone_number', 'description',)
    inlines = [
        SiteInline,
    ]


admin.site.register(Customer, CustomerAdmin)
