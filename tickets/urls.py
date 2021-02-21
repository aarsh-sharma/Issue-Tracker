from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('list', listTickets, name='listTickets'),
    path('board_view', boardView, name='boardView'),
    path('create', createTicket, name='createTicket'),
    path('ticket/<int:tid>', ticketDetail, name='ticketDetail'),
    path('register', registerUser, name='registerUser'),
    path('login', loginUser, name='loginUser'),
    path('logout', logoutUser, name='logoutUser'),
    path('generate-excel/', exportTicketsAsExcel, name="generateExcel")
]
