from django.db import models
from django.contrib.auth.models import User
from rides.models import Ride


class Booking(models.Model):

    STATUS_CHOICES = [
        ('BOOKED', 'Booked'),
        ('CANCELLED', 'Cancelled'),
    ]

    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    passenger = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='BOOKED')

    def __str__(self):
        return f"{self.passenger.username} - {self.ride} - {self.status}"