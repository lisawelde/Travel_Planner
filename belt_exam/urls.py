from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
   	path('dashboard', views.dashboard),
    path('add_trip', views.add_trip),
    path('create_trip', views.create_trip),
    path('show_trip/<trip_id>', views.show_trip),
    path('join_trip/<trip_id>', views.join_trip),
    path('logout', views.logout),
]
