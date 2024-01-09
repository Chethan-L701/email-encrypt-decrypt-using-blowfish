import imaplib
from algo import decrypt_msg
import sys
import json

keys = {}
with open("./keys.json", "r") as f:
    keys = json.load(f)

sender_email = keys['sender_email']
receipient_email = keys['receipient_email']
receipient_auth = keys['receipient_auth']
subject = keys['subject']
imap_url = 'imap.gmail.com'

try:
    con = imaplib.IMAP4_SSL(imap_url)
    affirm = con.login(receipient_email, receipient_auth)
    print(f"{affirm}")
    con.select('Inbox')
    print("Selected inbox")
except:
    print(f"failed to connect to the {receipient_email}")
    sys.exit(0)


def get_mails() -> bytes:
    _, data = con.search(
        None, 'FROM "{}" SUBJECT {}'.format(sender_email, subject))
    return data[-1]


def get_encrypted_messages(email_num: bytes):
    nums: list = [num for num in str(email_num).split("'")[1].split()]
    data: list = []

    for num in nums:
        _, (d, _) = con.fetch(num, '(RFC822)')
        if d != None:
            message = str(d[1])[1:-2]
            vals = [val for val in message.split(
                '\\') if val != "r" and val != "n" and val != '']
            message = vals[-1]
            data.append(message[1:])
    return data


messages: list = get_encrypted_messages(get_mails())

print(f"complete conversation with {sender_email} on the subject {subject} in order of oldest to newest : ")
for message in messages:
    print("="*50)
    print(f"Encrypted Message : {message}")
    print(f"Decrypted Message : {decrypt_msg(message)}")
    print("="*50)
