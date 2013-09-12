from django.db import models

class UserBio(models.Model):
    email = models.EmailField(unique=True)
    bio = models.TextField()
    name = models.TextField()
    avatar = models.TextField()
    date_added = models.DateTimeField()
    date_updated = models.DateTimeField()
    date_deleted = models.DateTimeField(null=True, blank=True)
