from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ride
from datetime import datetime

class RideTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_create_ride(self):
        ride = Ride.objects.create(
            driver=self.user,
            pickup_location="Dublin",
            destination="Cork",
            ride_date=datetime.now(),
            seats_available=3,
            price=10.00
        )

        self.assertEqual(ride.pickup_location, "Dublin")
        self.assertEqual(ride.seats_available, 3)