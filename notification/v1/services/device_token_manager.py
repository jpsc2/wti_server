from fcm_django.models import FCMDevice



class DeviceTokenManager(object):

    def __init__(self, user, token):
        self.user = user
        self.token = token
        
    def perform_task(self):
        """ ----- """
        fcm_token = FCMDevice.objects.filter(registration_id=self.token).first()
        if fcm_token:
            fcm_token.user = self.user
            fcm_token.save()
        else:
            fcm_device = FCMDevice.objects.filter(user=self.user).update(active=False)
            fcm_device = FCMDevice()
            fcm_device.registration_id = self.token
            fcm_device.user = self.user
            fcm_device.active = True
            fcm_device.save()
        return True