from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from rides.models import Ride
import stripe
from django.conf import settings
from django.urls import reverse


# -------------------- BOOK RIDE (OLD - KEEP OPTIONAL) --------------------
@login_required
def bookride(request, ride_id):
    ride = Ride.objects.get(id=ride_id)

    if Booking.objects.filter(ride=ride, passenger=request.user).exists():
        messages.error(request, "You already booked this ride.")
        return redirect("searchride")

    if ride.seats_available <= 0:
        messages.error(request, "No seats available.")
        return redirect("searchride")

    Booking.objects.create(
        ride=ride,
        passenger=request.user
    )

    ride.seats_available -= 1
    ride.save()

    messages.success(request, "Ride booked successfully!")

    return redirect("mybookings")


# -------------------- MY BOOKINGS --------------------
@login_required
def mybookings(request):
    bookings = Booking.objects.filter(passenger=request.user)
    return render(request, "mybookings.html", {"bookings": bookings})


# -------------------- CANCEL BOOKING --------------------
@login_required
def cancelbooking(request, id):
    booking = Booking.objects.get(id=id)

    if booking.passenger != request.user:
        return redirect("mybookings")

    ride = booking.ride

    ride.seats_available += 1
    ride.save()

    booking.status = 'CANCELLED'
    booking.save()

    messages.success(request, "Booking cancelled successfully!")

    return redirect("mybookings")


# -------------------- STRIPE PAYMENT --------------------
@login_required
def create_checkout_session(request, ride_id):
    ride = Ride.objects.get(id=ride_id)

    stripe.api_key = settings.STRIPE_SECRET_KEY

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': f"Ride from {ride.pickup_location} to {ride.destination}",
                },
                'unit_amount': int(ride.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',

        # ✅ FIXED SUCCESS URL
        success_url=request.build_absolute_uri(
            reverse('payment_success', args=[ride.id])
        ),

        # ✅ OPTIONAL CANCEL PAGE
        cancel_url=request.build_absolute_uri(
            reverse('payment_cancel')
        ),
    )

    return redirect(session.url)


# -------------------- PAYMENT SUCCESS --------------------
@login_required
@login_required
def payment_success(request, ride_id):
    ride = Ride.objects.get(id=ride_id)

    if Booking.objects.filter(ride=ride, passenger=request.user).exists():
        return render(request, "payment_success.html", {"ride": ride})

    if ride.seats_available <= 0:
        messages.error(request, "No seats available.")
        return redirect("searchride")

    Booking.objects.create(
    ride=ride,
    passenger=request.user,
    status='BOOKED'

    )

    ride.seats_available -= 1
    ride.save()

    return render(request, "payment_success.html", {"ride": ride})


# -------------------- PAYMENT CANCEL --------------------
@login_required
def payment_cancel(request):
    messages.error(request, "Payment cancelled.")
    return redirect("searchride")
@login_required
def payment_history(request):
    bookings = Booking.objects.filter(passenger=request.user).order_by('-booking_date')
    return render(request, "payment_history.html", {"bookings": bookings})