from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User
from rides.models import Ride


class Booking(models.Model):

    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    passenger = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.passenger.username} booked {self.ride}"