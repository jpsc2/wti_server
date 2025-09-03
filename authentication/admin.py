from django.contrib import admin
from authentication.models import UserCustomerMapping,  UserSiteMapping, UserDeviceMapping
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class UserCustomerMappingAdmin(admin.ModelAdmin):
    list_display = ('user',)


class UserSiteMappingAdmin(admin.ModelAdmin):
    list_display = ('user',)


class UserDeviceMappingAdmin(admin.ModelAdmin):
    list_display = ('user',)


class UserCustomerMappingInline(admin.TabularInline):
    model = UserCustomerMapping


class UserSiteMappingInline(admin.TabularInline):
    model = UserSiteMapping


class UserDeviceMappingInline(admin.TabularInline):
    model = UserDeviceMapping


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser')
    inlines = [
        UserCustomerMappingInline,
        UserSiteMappingInline,
        UserDeviceMappingInline
    ]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserCustomerMapping, UserCustomerMappingAdmin)
admin.site.register(UserSiteMapping, UserSiteMappingAdmin)
admin.site.register(UserDeviceMapping, UserDeviceMappingAdmin)

