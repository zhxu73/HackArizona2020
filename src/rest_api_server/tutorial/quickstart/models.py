from django.db import models

class UserData(models.Model):

    #id = models.IntegerField(unique=True)
    sessionId = models.CharField(max_length=256)
    departure_time = models.DateTimeField(null=True)
    # departure city
    city = models.CharField(max_length=256, null=True)
    # departure airport
    airport = models.CharField(max_length=10, null=True)
    #arrival_time = models.DateTimeField(null=True)
    flight_number = models.CharField(max_length=15, null=True)
    price = models.IntegerField(null=True)
    currency = models.CharField(max_length=10, null=True)
    flight_json = models.CharField(max_length=1000, null=True)
