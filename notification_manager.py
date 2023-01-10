import os
import dotenv
from twilio.rest import Client
import smtplib


class NotificationManager:

    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        dotenv.load_dotenv()
        self.twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
        self.recipient_phone_number = "+12197072088"
        self.client = Client(self.twilio_account_sid, self.twilio_auth_token)
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_email_password = os.getenv("SENDER_EMAIL_PASSWORD")

    def send_text_message(self, message):
        self.client.messages.create(
            body=f"\n{message}",
            from_=self.twilio_phone_number,
            to=self.recipient_phone_number
        )

    def send_email(self, recipient_email, subject, body):
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=self.sender_email, password=self.sender_email_password)
            connection.sendmail(from_addr=self.sender_email,
                                to_addrs=recipient_email,
                                msg=f"Subject:{subject}\n\n{body}")
