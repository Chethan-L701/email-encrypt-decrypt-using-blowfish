import smtplib
from email.mime.text import MIMEText
from algo import encrypt_msg
import json


keys = {}
with open("./keys.json", "r") as f:
    keys = json.load(f)

sender_email = keys['sender_email']
receipient_email = keys['receipient_email']
sender_auth = keys['sender_auth']

subject = keys['subject']

message = input("Enter message to send: ").strip()
encrypted_msg = encrypt_msg(message)

msg = MIMEText(encrypted_msg)
msg['Subject'] = subject
msg['From'] = sender_email
msg['To'] = receipient_email

print("\nSending email ...\n")
print("----------------------------")
print("From:\t", msg['From'])
print("To:\t", msg['To'])
print("Subject:", msg['Subject'])
print("Message:\n", encrypted_msg)
print("----------------------------")
print("\nMessage sent ... ", u'\u2713')

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
server.login(sender_email, sender_auth)
server.sendmail(sender_email, receipient_email, (msg.as_string()))
server.quit()
