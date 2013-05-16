from django.db import models

class UserSignup(models.Model):
    email = models.EmailField(unique=True)
    invite_code = models.CharField(max_length=64)
    questions = models.TextField()
    # TODO this field is used to determine if a signup is new, consider renaming!
    date_welcome_email_sent = models.DateTimeField(null=True, blank=True)
    sequence = models.IntegerField()
    date_added = models.DateTimeField()
    date_updated = models.DateTimeField()
