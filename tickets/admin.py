from django.contrib import admin

from .models import Ticket, TicketComments

# Register your models here.

admin.site.register(Ticket)
admin.site.register(TicketComments)
