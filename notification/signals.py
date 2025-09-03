from django.db.models.signals import post_save
from django.dispatch import receiver
from notification.models import Notification
from notification.v1.services.push_notification_service import SendPushNotification

@receiver(post_save, sender=Notification)
def notification_created(sender, instance: Notification, created, **kwargs):
    if created and not getattr(instance, "_skip_signal", False):
        try:
            SendPushNotification(
                device_id=instance.device.mac if instance.device else None,
                message=instance.subtitle or instance.title,
                flag=1
            ).perform_task()
        except Exception as e:
            print("Error sending push:", e)
