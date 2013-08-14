import imaplib
from email.parser import HeaderParser
from django.conf import settings

def get_emails():
    conn = imaplib.IMAP4('imap.mailgun.org')
    conn.login('the-machine@mechanicalmooc.org', settings.MAILBOX_PASSWORD)
    conn.select()
    conn.search(None, 'ALL') # returns a nice list of messages...

    data = conn.fetch('1:*', '(BODY[HEADER])')

    print(len(data[1]))

    message_fields = ['From', 'To', 'Subject', 'Date']
    messages = []
    for i in range(0, len(data[1]), 2):
        print(i)
        header_data = data[1][i][1]
        #print(header_data)
        parser = HeaderParser()
        msg = parser.parsestr(header_data)
        messages += [ { key: msg[key] for key in message_fields } ]
    return messages
