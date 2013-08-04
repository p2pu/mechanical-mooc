import api
import db
from utils import parse_timestamp

import hashlib
import json

def download_logs():
    """ Download mailgun logs and store them in the database """
    logs = []
    skip = 0
    
    # Fetch all unsaved logs and add them to a LIFO queue 
    while True:
        print("fecthing logs starting at {}".format(skip))
        for log in api.get_logs(limit=100, skip=skip)['items']:
            log_data = json.dumps(log)
            log_hash = hashlib.sha256(log_data).hexdigest()
            if db.MailgunLog.objects.filter(log_hash=log_hash).exists():
                break
            else:
                logs[:0] = [(log_hash, log_data, parse_timestamp(log['date_created']]
        else: 
            break
        skip += 100

    # take items from LIFO queue and save to db
    for log_hash, data, timestamp in logs:
        db.MailgunLog(
            log_hash=log_hash,
            data=data,
            timestamp=timestamp
        ).save()
