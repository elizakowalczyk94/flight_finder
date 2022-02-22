import smtplib
import ssl
import os

import pandas
from dotenv import load_dotenv

load_dotenv("venv/.env")

EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
USER_DATA_CSV = "users_data.csv"


class NotificationManager:

    def __init__(self):
        self.port = 465
        self.smtp_server = "smtp.gmail.com"
        self.sender_email = SENDER_EMAIL
        self.password = EMAIL_PASSWORD
        self.email_message = ""
        self.receivers_emails = []
        self.read_users_data()

    def send_email(self, message, receiver_email):
        self.email_message = f"Subject: Flight alert \n\n {message}"
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, receiver_email, self.email_message)

    def read_users_data(self):
        users_data = pandas.read_csv(USER_DATA_CSV)
        self.receivers_emails = users_data.user_email.tolist()

    def send_email_to_all_users(self, message):
        for user_email in self.receivers_emails:
            self.send_email(message, user_email)
