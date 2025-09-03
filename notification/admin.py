from django.contrib import admin
from notification.models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'subtitle', 'action','device')


admin.site.register(Notification, NotificationAdmin)
