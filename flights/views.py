from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Flight, Passenger


# Create your views here.
def index(request):
    """
    List all flights by interacting with the classes instead of SQL queries.
    """
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })

def flight(request, flight_id):
    flight = Flight.objects.get(pk=flight_id)
    return render(request, "flights/flight.html", {
        "flight": flight, 
        "passengers": flight.passengers.all(),
        # Because passengers is a related_name, we can take a flight and get all it's passengers
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
        # Exclude all passengers that are already on the flight
    })

def book(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(pk= flight_id)
        # For a passenger that already exists, add the flight to their flights column.
        passenger = Passenger.objects.get(pk = int(request.POST["passenger"]))
        passenger.flights.add(flight)
        return redirect(reverse("flight", args=(flight.id,)))