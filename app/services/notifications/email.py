import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from services.notifications.base import NotificationChannel

class EmailNotificationChannel(NotificationChannel):
    def __init__(self):
        # Replace with your email credentials and settings
        self.sender_email = os.environ.get("SMTP_EMAIL")
        self.sender_password = os.environ.get("SMTP_PASSWORD")
        self.smtp_server = os.environ.get("SMTP_SERVER")
        self.smtp_port = os.environ.get("SMTP_PORT")


    def send_message(self, to_email, subject, body):
        # Create the email message
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = to_email
        message["Subject"] = subject

        # Attach the body of the email
        message.attach(MIMEText(body, "plain"))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, to_email, message.as_string())

