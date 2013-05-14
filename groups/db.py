from django.db import models

class Group(models.Model):
    address = models.EmailField(unique=True)
    description = models.CharField(max_length=255)
    sequence = models.CharField(max_length=255)


class GroupMember(models.Model):
    email = models.EmailField()
    group = models.ForeignKey(Group, related_name='members')
