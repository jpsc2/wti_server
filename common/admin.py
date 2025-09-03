from django.contrib import admin
from common.models import AdministratorEmail


# Register your models here.

class AdministratorEmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'description')


admin.site.register(AdministratorEmail, AdministratorEmailAdmin)
