import unittest
from unittest.mock import MagicMock, patch
from services.notifications.email import EmailNotificationChannel

class TestEmailNotificationChannel(unittest.TestCase):

    @patch('smtplib.SMTP')
    def test_send_message(self, mock_smtp):
        # Arrange
        # Create a mock SMTP instance
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_smtp_instance

        email_channel = EmailNotificationChannel()
        to_email = 'recipient@example.com'
        subject = 'Test Subject'
        body = 'Test Body'

        # Act
        email_channel.send_message(to_email, subject, body)

        # Assert
        # Ensure SMTP server is initialized with the correct parameters
        mock_smtp.assert_called_once_with(email_channel.smtp_server, email_channel.smtp_port)

        # Ensure starttls and login are called on the SMTP server instance
        mock_smtp_instance.starttls.assert_called_once()
        mock_smtp_instance.login.assert_called_once_with(email_channel.sender_email, email_channel.sender_password)

        # Ensure sendmail is called
        mock_smtp_instance.sendmail.assert_called_once()