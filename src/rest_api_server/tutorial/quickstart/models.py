from django.db import models

class UserData(models.Model):

    #id = models.IntegerField(unique=True)
    sessionId = models.CharField(max_length=256)
    departure_time = models.DateTimeField()
    # departure city
    city = models.CharField(max_length=256, null=True)
    # departure airport
    airport = models.CharField(max_length=10, null=True)
    arrival_time = models.DateTimeField(null=True)
    flight_number = models.CharField(max_length=15, null=True)
    price = models.IntegerField(null=True)
    currency = models.CharField(max_length=10, null=True)
    flight_json = models.CharField(max_length=1000, null=True)

    @property
    def sessionId(self):
        return self.sessionId
    @property
    def departure_time(self):
        return self.departure_time
    @property
    def city(self):
        return self.city
    @property
    def airport(self):
        return self.airport
    @property
    def arrival_time(self):
        return self.arrival_time
    @property
    def flight_number(self):
        return self.flight_number
    @property
    def price(self):
        return self.price
    @property
    def currency(self):
        return self.currency
    @property
    def flight_json(self):
        return self.flight_json


    def complete(self):
        """
        return True if and only if all field are filled
        """
        if not self.session:
            return False
        if not self.departure_time:
            return False
        if not self.city:
            return False
        if not self.airport:
            return False
        if not self.arrival_time:
            return False
        if not self.flight_number:
            return False
        if not self.price:
            return False
        if not self.currency:
            return False
        if not self.flight_json:
            return False
        return True

    class Meta:
        db_table = "user_data"
        app_label = "quickstart"

