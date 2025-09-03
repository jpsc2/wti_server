from devices.models import Devices
from authentication.models import UserCustomerMapping, UserSiteMapping, UserDeviceMapping
from fcm_django.models import FCMDevice
from notification.models import Notification
from firebase_admin import messaging

MAX_LENGTH = 250  # DB limit

class SendPushNotification:

    def __init__(self, device_id, message, flag):
        self.device_id = device_id
        self.message = message
        self.flag = flag
        self.device_data = self.get_device()

    def get_device(self):
        return Devices.objects.get(mac=self.device_id)

    def _users(self):
        customerMapping = UserCustomerMapping.objects.filter(customers__in=[self.device_data.site.customer])
        sitesMapping = UserSiteMapping.objects.filter(sites__in=[self.device_data.site])
        deviceMapping = UserDeviceMapping.objects.filter(devices__in=[self.device_data])

        users = {x.user for x in customerMapping} | {x.user for x in sitesMapping} | {x.user for x in deviceMapping}
        return list(users)

    def _create_notification(self, user):
        # Include device id in title and subtitle
        title = f"{self.device_data.name} {self.device_data.mac} {self.message}"[:MAX_LENGTH]
        subtitle = f"{self.device_data.name} {self.device_data.mac} {self.message}"[:MAX_LENGTH]

        notification = Notification(
            user=user,
            image="https://static.vecteezy.com/system/resources/previews/015/402/523/original/stop-fan-illustration-on-a-background-premium-quality-symbols-icons-for-concept-and-graphic-design-vector.jpg",
            title=title,
            subtitle=subtitle,
            action="CRITICAL_FAILURE",
            device=self.device_data
        )
        # Skip signal to prevent recursion
        notification._skip_signal = True
        notification.save()
        return notification
    
    def perform_task(self):
        users = self._users()
        results = {}

        for user in users:
            notification = self._create_notification(user)

            # Send push to active, unique FCM devices only
            fcm_devices = FCMDevice.objects.filter(user=user, active=True).distinct('registration_id')
            results[user.username] = []

            for fcm_device in fcm_devices:
                try:
                    message = messaging.Message(
                        notification=messaging.Notification(
                            title=notification.title,
                            body=notification.subtitle,
                            image=notification.image
                        ),
                        data={
                            "title": notification.title,
                            "body": notification.subtitle,
                            "image": notification.image,
                        },
                        token=fcm_device.registration_id
                    )
                    response = messaging.send(message)
                    results[user.username].append({"status": "success", "response": str(response)})
                except Exception as e:
                    results[user.username].append({"status": "failed", "error": str(e)})

        return {"results": results}
