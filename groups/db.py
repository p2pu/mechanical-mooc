from django.db import models

class Group(models.Model):
    address = models.EmailField(unique=True)
    description = models.CharField(max_length=255)
    sequence = models.IntegerField()
    #NOTE: do we need date_created and date_removed?


class GroupMember(models.Model):
    email = models.EmailField()
    group = models.ForeignKey(Group, related_name='members')
    #NOTE: do we need date_added and date_removed?
