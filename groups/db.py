from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=255)


class GroupMember(models.Model):
    email = models.EmailField()
    group = models.ForeignKey(Group, related_name='members')
