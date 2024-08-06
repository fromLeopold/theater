from datetime import timedelta
from decimal import Decimal

from django.db.models import Sum
from django.utils.timezone import now, localtime

from admin_panel.models import DailyPerformanceStatistics, DailyTimeStatistics
from poster.models import Performance


def get_interval(hour):
    if 0 <= hour < 3:
        return '0-3'
    elif 3 <= hour < 6:
        return '3-6'
    elif 6 <= hour < 9:
        return '6-9'
    elif 9 <= hour < 12:
        return '9-12'
    elif 12 <= hour < 15:
        return '12-15'
    elif 15 <= hour < 18:
        return '15-18'
    elif 18 <= hour < 21:
        return '18-21'
    else:
        return None


def get_performances_popularity():
    start_of_last_month = now() - timedelta(days=30)
    performances_popularity = DailyPerformanceStatistics.objects.filter(
        date__gte=start_of_last_month
    ).values('performance__name').annotate(
        total_sold_tickets=Sum('sold_tickets'),
        total_revenue=Sum('revenue')
    ).order_by('-total_sold_tickets', '-total_revenue')
    return performances_popularity


def get_time_popularity():
    one_month_ago = now() - timedelta(days=30)
    statistics = DailyTimeStatistics.objects.filter(date__gte=one_month_ago)
    interval_data = {}

    for stat in statistics:
        local_date = localtime(stat.date)
        interval = get_interval(local_date.hour)
        if interval:
            if interval not in interval_data:
                interval_data[interval] = {
                    'total_sold_tickets': 0,
                    'total_revenue': Decimal('0.00')
                }
            interval_data[interval]['total_sold_tickets'] += stat.sold_tickets
            interval_data[interval]['total_revenue'] += stat.revenue

    sorted_intervals = sorted(interval_data.items(),
                              key=lambda x: (-x[1]['total_sold_tickets'], -x[1]['total_revenue']))
    return sorted_intervals


def get_top_performances():
    performance_stats = DailyPerformanceStatistics.objects.values('performance__id') \
        .annotate(total_sold_tickets=Sum('sold_tickets')) \
        .order_by('-total_sold_tickets')
    max_tickets = performance_stats.first()['total_sold_tickets'] if performance_stats else 0
    top_performance_ids = performance_stats.filter(total_sold_tickets=max_tickets) \
        .values_list('performance__id', flat=True)
    top_performances = Performance.objects.filter(id__in=top_performance_ids)
    return top_performances


def get_least_popular_performances():
    performance_stats = DailyPerformanceStatistics.objects.values('performance__id') \
        .annotate(total_sold_tickets=Sum('sold_tickets')) \
        .order_by('total_sold_tickets')
    min_tickets = performance_stats.first()['total_sold_tickets'] if performance_stats else 0
    least_popular_performance_ids = performance_stats.filter(total_sold_tickets=min_tickets).values_list('performance__id', flat=True)
    least_popular_performances = Performance.objects.filter(id__in=least_popular_performance_ids)
    return least_popular_performances

