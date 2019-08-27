from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
	return render(request, "index.html")

def register(request):
    errors = User.objects.regValidator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        new_user = User.objects.create(first_name=request.POST["first_name"], last_name=request.POST["last_name"], username=request.POST["username"], password=hashed_pw.decode())

        request.session['id'] = new_user.id
        return redirect('/dashboard')

def login(request):
    errors = User.objects.loginValidator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user_list = User.objects.filter(username=request.POST['username'])
        user = user_list[0]
        request.session['id'] = user.id
        return redirect('/dashboard')

def dashboard(request):
    if 'id' not in request.session:
        return redirect("/")
    else:
        user = User.objects.get(id=request.session["id"])
        all_trips = Trip.objects.all()
        user_trips = user.joined_trips.all()
        other_user_trips = all_trips.difference(user_trips)
        context = {
            'user': user,
            'confirmed_trips': user_trips,
            'other_trips': other_user_trips,
        }
        return render(request, "dashboard.html", context)

def add_trip(request):
    if 'id' not in request.session:
        return redirect("/")
    else:
        return render(request, "add_trip.html")

def create_trip(request):
    errors = Trip.objects.tripValidator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/add_trip')
    else:
        trip = Trip.objects.create(destination=request.POST["destination"], description=request.POST["description"], travel_from=request.POST["travel_from"], travel_to=request.POST["travel_to"], added_by_id=request.session['id'])
        user = User.objects.get(id=request.session["id"])
        user.joined_trips.add(trip)

        return redirect('/dashboard')

def show_trip(request, trip_id):
    if 'id' not in request.session:
        return redirect("/")
    else:
        user = User.objects.get(id=request.session["id"])
        trip = Trip.objects.get(id=trip_id)
        users_who_join = trip.users_who_join.exclude(id=trip.added_by_id)
        trips_user_joined = user.joined_trips.all()
        context = {
            'user': user,
            "trip": trip,
            'users': users_who_join,
            'trips': trips_user_joined,
        }
        return render(request, "show_trip.html", context)

def join_trip(request, trip_id):
    user = User.objects.get(id=request.session["id"])
    trip = Trip.objects.get(id=trip_id)
    user.joined_trips.add(trip)
    return redirect("/dashboard")

def logout(request):
    request.session.clear()
    return redirect("/")
