from django.test import TestCase
from django.contrib.auth.models import User
from rides.models import Ride
from .models import Booking
from datetime import datetime


class BookingTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")  # nosec
        self.ride = Ride.objects.create(
            driver=self.user,
            pickup_location="Dublin",
            destination="Cork",
            ride_date=datetime.now(),
            seats_available=3,
            price=10.00
        )

    def test_booking_creation(self):
        booking = Booking.objects.create(
            ride=self.ride,
            passenger=self.user
        )

        self.assertEqual(booking.status, "BOOKED")