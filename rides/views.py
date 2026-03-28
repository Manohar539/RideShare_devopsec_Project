from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Ride
from .forms import RideForm

def home(request):
    return render(request, "home.html")

@login_required
def dashboard(request):
    return render(request, "dashboard.html")

def ridelist(request):
    rides = Ride.objects.all()
    return render(request, "ridelist.html", {"rides": rides})

@login_required
def createride(request):

    if request.method == "POST":
        form = RideForm(request.POST)

        if form.is_valid():
            ride = form.save(commit=False)
            ride.driver = request.user  
            ride.save()
            messages.success(request, "Ride created successfully!")
            return redirect("searchride")

    else:
        form = RideForm()

    return render(request, "createride.html", {"form": form})

@login_required
def updateride(request, id):

    ride = get_object_or_404(Ride, id=id)
    if ride.driver != request.user:
        messages.error(request, "You are not allowed to edit this ride.")
        return redirect("ridelist")

    if request.method == "POST":
        form = RideForm(request.POST, instance=ride)

        if form.is_valid():
            form.save()
            messages.success(request, "Ride updated successfully!")
            return redirect("ridelist")

    else:
        form = RideForm(instance=ride)

    return render(request, "updateride.html", {"form": form})

@login_required
def deleteride(request, id):

    ride = get_object_or_404(Ride, id=id)
    if ride.driver != request.user:
        messages.error(request, "You are not allowed to delete this ride.")
        return redirect("ridelist")

    ride.delete()
    messages.success(request, "Ride deleted successfully!")

    return redirect("ridelist")


@login_required
def searchride(request):

    pickup = request.GET.get("pickup")
    destination = request.GET.get("destination")

    rides = Ride.objects.all()

    if pickup:
        rides = rides.filter(pickup_location__icontains=pickup)

    if destination:
        rides = rides.filter(destination__icontains=destination)

    return render(request, "searchride.html", {"rides": rides})