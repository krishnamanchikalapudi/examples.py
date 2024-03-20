from twilio.rest import Client
from datetime import datetime

format_string = "%m-%d-%Y %H:%M:%S"
dateTimeObj = datetime.now()
timestampStr = dateTimeObj.strftime(format_string)
print('Current Timestamp : ', timestampStr)

# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'auth_sid'
auth_token = 'auth_token'
client = Client(account_sid, auth_token)

message = client.messages.create(
                              body=('Hello there from Python! at '+timestampStr),
                              from_='whatsapp:+1234567890',
                              to='whatsapp:+1987654321'
                          )

print(message.sid)

print("Message sent")
exit(0);
