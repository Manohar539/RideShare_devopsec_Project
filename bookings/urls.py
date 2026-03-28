from django.urls import path
from . import views

urlpatterns = [
    path("book/<int:ride_id>/", views.bookride, name="bookride"),
    path("mybookings/", views.mybookings, name="mybookings"),
    path("cancel/<int:id>/", views.cancelbooking, name="cancelbooking"),
    path("pay/<int:ride_id>/", views.create_checkout_session, name="payment"),
    path("success/<int:ride_id>/", views.payment_success, name="payment_success"),    path("cancel/", views.payment_cancel, name="payment_cancel"),
    path("payments/", views.payment_history, name="payment_history"),
    path('payment-success/<int:ride_id>/', views.payment_success, name='payment_success'),
]