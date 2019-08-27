from django.db import models
from datetime import datetime, timedelta
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NOW = str(datetime.now())

class UserManager(models.Manager):
    def regValidator(self, form):
        errors = {}
        if not form['first_name']:
            errors['first_name'] = "Please enter a first name."
        elif len(form['first_name']) < 3:
            errors['first_name'] = "First name must be at least three characters."

        if not form['last_name']:
            errors['last_name'] = "Please enter a last name."
        elif len(form['last_name']) < 3:
            errors['last_name'] = "Last name must be at least three characters."

        if not form['username']:
            errors['username'] = "Please enter a username."
        elif len(form['username']) < 3:
            errors['username'] = "Username must be at least three characters."
        elif User.objects.filter(username=form["username"]):
            errors['username'] = "Username already in database, please login."

        if not form['password']:
            errors['password'] = "Please enter a password."
        elif len(form['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."

        if not form['confirm_password']:
            errors['confirm_password'] = "Please enter a confirm password."
        elif form['confirm_password'] != form['password']:
            errors['confirm_password'] = "Passwords must match."

        return errors

    def loginValidator(self, form):
        errors = {}

        if not form['username']:
            errors['username'] = "Please enter a username."
        elif len(form['username']) < 3:
            errors['username'] = "Username must be at least three characters."
        elif not User.objects.filter(username=form["username"]):
            errors['username'] = "Username not found. Please register."
        else:
            user_list = User.objects.filter(username=form["username"])
            user = user_list[0]
            if not form['password']:
                errors['password'] = "Please enter a password."
            if not bcrypt.checkpw(form['password'].encode(), user.password.encode()):
                errors['password'] = "Wrong password."
        return errors


class TripManager(models.Manager):
    def tripValidator(self, form):
        errors = {}
        if not form['destination']:
            errors['destination'] = "Please enter a destination."
        
        if not form['description']:
            errors['description'] = "Please enter a description."

        if not form['travel_from']:
            errors['travel_from'] = "Please enter a travel from date."
        elif form['travel_from'] < NOW:
            errors['travel_from'] = "Travel from date must be in the future."

        if not form['travel_to']:
            errors['travel_to'] = "Please enter a travel to date."
        elif form['travel_to'] < form['travel_from']:
            errors['travel_to'] = "Travel to date must be after travel from date."

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    # joined_trips = a list of trips a given user joins
    # trips_added = a list of trips added by a given user

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField()
    travel_from = models.DateTimeField()
    travel_to = models.DateTimeField()
    added_by = models.ForeignKey(User, related_name="trips_added", on_delete=models.CASCADE) # the user who added a given trip
    users_who_join = models.ManyToManyField(User, related_name="joined_trips") # a list of users who join a given trip
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
