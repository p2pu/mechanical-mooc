from django.conf import settings

import datetime
import base64
import hmac, hashlib


def create_s3_policy_doc(bucket, upload_path, redirect, max_file_size=2**20):
    policy_template = """{{"expiration": "{expiration_date}",
  "conditions": [ 
    {{"bucket": "{bucket}"}}, 
    ["starts-with", "$key", "{upload_path}"],
    {{"acl": "public-read"}},
    {{"success_action_status": "201"}},
    ["starts-with", "$Content-Type", ""],
    ["content-length-range", 0, {max_file_size}]
  ]
}}"""

    expiration_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    policy_doc = policy_template.format(
        expiration_date=expiration_date.strftime("%Y-%M-%dT%H:%m:%SZ"),
        bucket=bucket, 
        upload_path=upload_path,
        redirect=redirect,
        max_file_size=max_file_size
    )
    policy_b64 = base64.b64encode(policy_doc)
    signature = base64.b64encode(hmac.new(settings.AWS_SECRET_ACCESS_KEY, policy_b64, hashlib.sha1).digest())

    return policy_b64, signature
 
