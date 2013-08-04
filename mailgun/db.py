from django.db import models

class MailgunLog(models.Model):
    log_hash = models.CharField(max_length=64, unique=True)
    data = models.TextField()
    timestamp = models.DateTime()
