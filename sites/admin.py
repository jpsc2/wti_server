from django.contrib import admin
from sites.models import Site
from devices.models import Devices


class DevicesInline(admin.TabularInline):
    model = Devices


class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'customer',)
    inlines = [
        DevicesInline,
    ]


admin.site.register(Site, SiteAdmin)
