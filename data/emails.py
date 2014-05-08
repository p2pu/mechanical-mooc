from data.utils import write_to_csv

from django.conf import settings

import imaplib
import mailbox
from email import message_from_string
from datetime import datetime

def get_emails():
    """ Download all the raw emails from the IMAP server and return a list of email.message.Message """
    conn = imaplib.IMAP4('imap.mailgun.org')
    conn.login(settings.DEFAULT_FROM_EMAIL, settings.MAILBOX_PASSWORD)
    conn.select() # select inbox
    typ, message_ids = conn.uid('search', None, 'ALL') # get a list of all messages
    msg_count = len(message_ids[0].split())

    messages = []
    for i, uid in enumerate(message_ids[0].split()):
        print('Downloading message {0} of {1}'.format(i, msg_count))
        typ, data = conn.uid('fetch', uid, '(BODY[])')
        msg = message_from_string(data[0][1])
        messages += [msg]
    return messages


def process_messages(email_list):
    """ takes a list of messages and convert them to a format we can shove into CSV """
    message_fields = ['From', 'To', 'Subject', 'Date']
    messages = []
    for msg in email_list:
        message = { key: msg[key] for key in message_fields }
        body = ''
        if msg.is_multipart():
            # Make a best guess at the body of the message
            # 1. Use text/plain
            # 2. Use text/html
            for part in msg.walk():
                if body == '' and part.get_content_type() == 'text/html':
                    body = part.get_payload()
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload()
        else:
            body = msg.get_payload()
        message['body'] = body
        messages += [message]
    return messages


def export_emails(prefix=''):
    messages = get_emails()
    timestamp = datetime.now().date().isoformat()
    mb = mailbox.mbox('{0}_emails_{1}.mbox'.format(prefix, timestamp))
    for msg in messages:
        mb.add(msg)
    mb.close()
    csv_data = process_messages(messages)
    write_to_csv(csv_data, '{0}_emails_{1}.csv'.format(prefix, timestamp))

