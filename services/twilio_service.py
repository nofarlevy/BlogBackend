import os

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

account = os.environ.get('TWILIO_SID')
token = os.environ.get('TWILIO_TOKEN')
client = Client(account, token)


def send_message(message, to_phone):
    try:
        send_message = client.messages.create(
            to=to_phone,
            from_="+13342316784",
            body=message
        )

    except TwilioRestException as err:
        print(err)

send_message("Hey gal", "+972509191414")