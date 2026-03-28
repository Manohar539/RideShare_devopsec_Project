from django import forms
from .models import Ride

class RideForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = [
            "pickup_location",
            "destination",
            "ride_date",
            "seats_available",
            "price",
        ]
        widgets = {
            'ride_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }
        
    def clean_seats_available(self):
        seats = self.cleaned_data.get('seats_available')
        if seats is not None and seats <= 0:
            raise forms.ValidationError("Seats must be greater than 0")
        return seats

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be greater than 0")
        return price

    def clean(self):
        cleaned_data = super().clean()
        pickup = cleaned_data.get("pickup_location")
        destination = cleaned_data.get("destination")

        if pickup and destination and pickup.lower() == destination.lower():
            raise forms.ValidationError("Pickup and destination cannot be the same")

        return cleaned_data