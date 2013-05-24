from django.db import models

class UserSignup(models.Model):
    email = models.EmailField()
    invite_code = models.CharField(max_length=64)
    questions = models.TextField()
    sequence = models.IntegerField(null=True, blank=True)
    date_added = models.DateTimeField()
    date_updated = models.DateTimeField()
    date_deleted = models.DateTimeField(null=True, blank=True)
    date_tasks_handled = models.DateTimeField(null=True, blank=True)
