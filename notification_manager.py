import smtplib
import ssl
import os
from dotenv import load_dotenv

load_dotenv("venv/.env")

EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")


class NotificationManager:

    def __init__(self, receiver_email, message):
        self.port = 465
        self.smtp_server = "smtp.gmail.com"
        self.sender_email = SENDER_EMAIL
        self.receiver_email = receiver_email
        self.password = EMAIL_PASSWORD
        self.message = message
        self.email_message = ""
        self.create_message()

    def create_message(self):
        self.email_message = f"Subject: Flight alert \n\n {self.message}"

    def send_email(self):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.receiver_email, self.email_message)
