from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('list', listTickets, name='list'),
    path('register', registerUser, name='registerUser'),
    path('login', loginUser, name='loginUser'),
    path('logout', logoutUser, name='logoutUser'),
]
