from notification.models import Notification


class NotificationList(object):
    def __init__(self, user):
        self.user = user
    
    def perform_task_and_get_data(self):
        notifications = list(Notification.objects.filter(user=self.user).order_by('id').values()[10:])
        notifications.reverse()
        return notifications
