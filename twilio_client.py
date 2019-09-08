import twilio.rest
import common

class TwilioClient:
    def __init__(self):
        self.account_sid = common.ACCOUNT_SID
        self.auth_token = common.AUTH_TOKEN

    def send_text(self, phone_number, content):
        # Your Account Sid and Auth Token from twilio.com/console
        # DANGER! This is insecure. See http://twil.io/secure
        client = twilio.rest.Client(self.account_sid, self.auth_token)

        message = client.messages \
            .create(
            body=content,
            from_='+18329247604',
            to=phone_number
        )
