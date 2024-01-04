from unittest import TestCase
from unittest.mock import patch

from services.notifications.base import NotificationService
from services.notifications.email import EmailNotificationChannel

class TestNotificationService(TestCase):

    @patch("services.notifications.email.EmailNotificationChannel.send_message")
    def test_notify(self, mocked_send_message):
        # send notification
        service = NotificationService()

        service.notify(
            EmailNotificationChannel,
            "somefakeemail@gmail.com",
            "Confirm patient registration",
            "Hello, name . Please confirm your registration."
        )

        mocked_send_message.assert_called_once_with(
            "somefakeemail@gmail.com",
            "Confirm patient registration",
            "Hello, name . Please confirm your registration."
        )

