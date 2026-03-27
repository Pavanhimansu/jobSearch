from twilio.rest import Client

# Your Twilio credentials
account_sid = 'AC51b2b005603c18a3c60a3940c60ffecb'
auth_token  = 'PASTE_YOUR_AUTH_TOKEN_HERE'   # from Twilio dashboard

client = Client(account_sid, auth_token)

# Simple plain text message — no content_sid or content_variables needed
message = client.messages.create(
    from_='whatsapp:+14155238886',
    body='Hello Pavan! JobHunt Bot test message. Setup working correctly! ✅',
    to='whatsapp:+919533852285'
)

print("Message sent! SID:", message.sid)
