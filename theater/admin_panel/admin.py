from django.contrib import admin
from .models import DailyPerformanceStatistics, DailyTimeStatistics


@admin.register(DailyPerformanceStatistics)
class DailyPerformanceStatisticsAdmin(admin.ModelAdmin):
    list_display = ('date', 'performance', 'total_tickets', 'sold_tickets', 'revenue', 'created_at')
    list_filter = ('date', 'performance')
    search_fields = ('performance__name',)


@admin.register(DailyTimeStatistics)
class DailyTimeStatisticsAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_tickets', 'sold_tickets', 'revenue', 'created_at')
    list_filter = ('date',)
    search_fields = ('date',)

