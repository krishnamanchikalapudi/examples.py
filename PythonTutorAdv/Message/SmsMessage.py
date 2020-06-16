from twilio.rest import Client
from datetime import datetime

format_string = "%m-%d-%Y %H:%M:%S"
dateTimeObj = datetime.now()
timestampStr = dateTimeObj.strftime(format_string)
print('Current Timestamp : ', timestampStr)

# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC1e5cd7e9389cd178250aa055f9274aa2'
auth_token = 'f18daa57ac3ad8c3a5f34e4f3ebe545f'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body=('Hello there from Python! sent at '+timestampStr),
                     from_='+12055576214',
                     to='+19258268473'
                 )

print(message.sid)