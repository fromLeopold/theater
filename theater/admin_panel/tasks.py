from celery import shared_task

from admin_panel.models import DailyPerformanceStatistics, DailyTimeStatistics
from poster.models import Performance, Session, Ticket
from django.db.models import Count, Sum
from datetime import timedelta, datetime
from django.utils import timezone


@shared_task
def collect_daily_performance_statistics():
    now = timezone.now()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)

    performances = Performance.objects.filter(repertoire=True)
    for performance in performances:
        sessions = Session.objects.filter(performance=performance, date__gte=start_of_day, date__lt=end_of_day)
        total_tickets = Ticket.objects.filter(session__in=sessions).count()
        sold_tickets = Ticket.objects.filter(session__in=sessions, sold=True).count()
        revenue = Ticket.objects.filter(session__in=sessions, sold=True).aggregate(Sum('price'))['price__sum'] or 0

        DailyPerformanceStatistics.objects.create(
            date=start_of_day.date(),
            performance=performance,
            total_tickets=total_tickets,
            sold_tickets=sold_tickets,
            revenue=revenue
        ).save()


@shared_task
def collect_daily_time_statistics():
    now = timezone.now()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)

    sessions = Session.objects.filter(date__gte=start_of_day, date__lt=end_of_day)
    for session in sessions:
        date = session.date
        total_tickets = Ticket.objects.filter(session=session).count()
        sold_tickets = Ticket.objects.filter(session=session, sold=True).count()
        revenue = Ticket.objects.filter(session=session, sold=True).aggregate(Sum('price'))['price__sum'] or 0

        DailyTimeStatistics.objects.create(
            date=date,
            total_tickets=total_tickets,
            sold_tickets=sold_tickets,
            revenue=revenue
        ).save()
