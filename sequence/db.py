from django.db import models

class Sequence(models.Model):
    signup_close_date = models.DateField()
    start_date = models.DateField()
