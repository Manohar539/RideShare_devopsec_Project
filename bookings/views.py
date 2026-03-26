from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.conf import settings

from .models import Booking
from rides.models import Ride

import stripe


# -------------------- BOOK RIDE (DIRECT BOOKING) --------------------
@login_required
def bookride(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id)

    # Prevent duplicate booking
    if Booking.objects.filter(ride=ride, passenger=request.user).exists():
        messages.error(request, "You already booked this ride.")
        return redirect("searchride")

    # Check seat availability
    if ride.seats_available <= 0:
        messages.error(request, "No seats available.")
        return redirect("searchride")

    # Create booking
    Booking.objects.create(
        ride=ride,
        passenger=request.user,
        status='BOOKED'
    )

    # Reduce seat count
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
    booking = get_object_or_404(Booking, id=id)

    if booking.passenger != request.user:
        return redirect("mybookings")

    ride = booking.ride

    # Restore seat
    ride.seats_available += 1
    ride.save()

    booking.status = 'CANCELLED'
    booking.save()

    messages.success(request, "Booking cancelled successfully!")
    return redirect("mybookings")


# -------------------- STRIPE PAYMENT --------------------
@login_required
def create_checkout_session(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id)

    stripe.api_key = settings.STRIPE_SECRET_KEY

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    # ✅ SAFE: using generic naming (won’t break if field names differ)
                    'name': f"Ride ID {ride.id}",
                },
                'unit_amount': int(ride.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',

        success_url=request.build_absolute_uri(
            reverse('payment_success', args=[ride.id])
        ),

        cancel_url=request.build_absolute_uri(
            reverse('payment_cancel')
        ),
    )

    return redirect(session.url)


# -------------------- PAYMENT SUCCESS --------------------
@login_required
def payment_success(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id)

    # Prevent duplicate booking
    if Booking.objects.filter(ride=ride, passenger=request.user).exists():
        return render(request, "payment_success.html", {"ride": ride})

    # Check seat availability
    if ride.seats_available <= 0:
        messages.error(request, "No seats available.")
        return redirect("searchride")

    # Create booking
    Booking.objects.create(
        ride=ride,
        passenger=request.user,
        status='BOOKED'
    )

    # Reduce seats
    ride.seats_available -= 1
    ride.save()

    return render(request, "payment_success.html", {"ride": ride})


# -------------------- PAYMENT CANCEL --------------------
@login_required
def payment_cancel(request):
    messages.error(request, "Payment cancelled.")
    return redirect("searchride")


# -------------------- PAYMENT HISTORY --------------------
@login_required
def payment_history(request):
    bookings = Booking.objects.filter(
        passenger=request.user
    ).order_by('-id')  # safer than booking_date if field missing

    return render(request, "payment_history.html", {"bookings": bookings})
