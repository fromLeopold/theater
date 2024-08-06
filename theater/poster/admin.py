from django.contrib import admin, messages

from poster.models import *


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'premiere', 'duration', 'start_date', 'expiration_date', 'repertoire']


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['pk', 'performance', 'date']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['pk', 'session', 'seat', 'reserved', 'sold', 'price']
    list_filter = ('reserved', 'sold')
    search_fields = ('user__username',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(reserved=False)

