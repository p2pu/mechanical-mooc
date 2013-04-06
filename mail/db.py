from django.db import models

class Email(models.Model):
    subject = models.CharField(max_length=255)
    text_body = models.TextField()
    html_body = models.TextField()


class Schedule(models.Model):
    date = models.DateTimeField()
    email = models.ForeignKey(Email)
