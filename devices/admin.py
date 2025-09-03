from django.contrib import admin
from devices.models import Devices, DeviceMaintenanceHistory
from authentication.models import UserDeviceMapping, UserSiteMapping


class DeviceMaintenanceHistoryInline(admin.TabularInline):
    model = DeviceMaintenanceHistory


class UserDeviceMappingInline(admin.TabularInline):
    model = UserDeviceMapping.devices.through


class DevicesAdmin(admin.ModelAdmin):
    list_display = ('name', 'mac', 'description', 'site','maintenance_date','longitude','latitude')
    inlines = [
        DeviceMaintenanceHistoryInline,
        UserDeviceMappingInline,
    ]


class DeviceMaintenanceHistoryAdmin(admin.ModelAdmin):
    list_display = ('device', 'remark','date','month_year','rating','supervisor','operator','remark')




admin.site.register(Devices, DevicesAdmin)
admin.site.register(DeviceMaintenanceHistory, DeviceMaintenanceHistoryAdmin)
