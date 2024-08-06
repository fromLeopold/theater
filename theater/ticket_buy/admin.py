from django.contrib import admin

from ticket_buy.models import *


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['pk', 'ticket', 'date_time', 'booking_number']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk', 'ticket', 'date_time', 'order_number']

