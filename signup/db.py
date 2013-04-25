from django.db import models

class UserSignup(models.Model):
    email = models.EmailField(unique=True)
    invite_code = models.CharField(max_length=64)
    questions = models.TextField()
    date_welcome_email_sent = models.DateTimeField(null=True, blank=True)
    date_added = models.DateTimeField()
    date_updated = models.DateTimeField()
