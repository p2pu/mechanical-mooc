from django.db import models

class Email(models.Model):
    subject = models.CharField(max_length=78)
    text_body = models.TextField()
    html_body = models.TextField()
    tags = models.CharField(max_length=1000)
    date_scheduled = models.DateTimeField(blank=True, null=True)
    date_sent = models.DateTimeField(blank=True, null=True)
