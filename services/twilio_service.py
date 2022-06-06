from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

account = "AC912a781e3b96d828739a3a82e3b6ba0f"
token = "094ffcbd0d5ac453c6f5abf57ddc1a8f"
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

