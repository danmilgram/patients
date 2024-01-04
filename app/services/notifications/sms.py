from services.notifications.base import NotificationChannel

class SmsNotificationChannel(NotificationChannel):
    def __init__(self):
        super().__init__()

    def send_message(*args):
        raise NotImplementedError()