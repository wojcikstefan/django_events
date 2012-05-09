from django.contrib.auth.models import User
from django.db import models

class Event(models.Model):
    created_by = models.ForeignKey(User)
    name = models.CharField(max_length=256)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    sales_end = models.DateTimeField()
    location = models.CharField(max_length=128) # preferrably changed to geo-location later
    description = models.TextField()
    private = models.BooleanField(default=False)
    
class Ticket(models.Model):
    event = models.ForeignKey(Event)
    name = models.CharField(max_length=64)
    description = models.TextField()
    available_quantity = models.IntegerField(null=True, blank=True)
    price = models.FloatField()
    