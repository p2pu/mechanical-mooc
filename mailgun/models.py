import api
import db
from utils import parse_timestamp
from django.db import transaction

from collections import OrderedDict

import hashlib
import json

@transaction.commit_manually
def download_logs():
    """ Download mailgun logs and store them in the database """
    # use ordered dict to protect against new logs arriving while downloading logs
    logs = OrderedDict()
    skip = 0
    
    # Fetch all unsaved logs and add them to a LIFO queue
    fetch_more = True
    while fetch_more:
        print("fecthing logs skip={}".format(skip))
        logs_tmp = api.get_logs(limit=1000, skip=skip)['items']
        if len(logs_tmp) == 0:
            break
        for log in logs_tmp:
            log_data = json.dumps(log)
            log_hash = hashlib.sha256(log_data).hexdigest()
            if db.MailgunLog.objects.filter(log_hash=log_hash).exists():
                fetch_more = False
                break
            else:
                logs[log_hash] = (log_hash, log_data, parse_timestamp(log['created_at']))
        skip += 1000

    # take items from LIFO queue and save to db
    print("Saving {0} logs to database".format(len(logs)))
    for i, (log_hash, data, timestamp) in enumerate(logs.values()):
        db.MailgunLog(
            log_hash=log_hash,
            data=data,
            timestamp=timestamp
        ).save()
        if (i+1) % 100 == 0:
            transaction.commit()
    transaction.commit()
