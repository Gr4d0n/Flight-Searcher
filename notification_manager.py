import os
from twilio.rest import Client
import smtplib

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ["TWILIO_AUTH_TOKEN"]

class NotificationManager:
    def __init__(self):
        self.smtp_address = os.environ['SMTP_ADDRESS']
        self.email = os.environ["MY_MAIL"]
        self.email_password = os.environ["MY_MAIL_PASSWORD"]

        self.client = Client(account_sid, auth_token)
        self.connection = smtplib.SMTP(os.environ['SMTP_ADDRESS'])

    def send_sms(self, message_body):
        message = self.client.messages.create(
            body=message_body,
            from_=os.environ["TWILIO_SMS_NUMBER"],
            to=os.environ['RECIEVER_NUMBER'],
        )

        # print(message.sid)

    def send_emails(self, email_list, email_body):
        with self.connection:
            self.connection.starttls()
            self.connection.login(self.email, self.email_password)
            for email in email_list:
                self.connection.sendmail(
                    from_addr=self.email,
                    to_addrs=email,
                    msg=f"Subject:New Price Flight!\n\n{email_body}".encode('utf-8')
                )


def formatting_price(price):
    formatted_price = ""
    price = str(price * 107)[::-1]
    index = 1
    for i in price:
        formatted_price += i
        if index % 2 != 0 and 2 < index < len(price):
            formatted_price += ','
        index += 1

    return formatted_price[::-1]
