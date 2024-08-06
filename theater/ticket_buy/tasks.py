from collections import defaultdict
from datetime import timezone, timedelta, datetime

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from ticket_buy.models import Order, Booking


@shared_task
def delete_tomorrow_bookings():
    tomorrow = timezone.now() + timedelta(days=1)
    start_of_tomorrow = timezone.make_aware(
        datetime.combine(tomorrow, datetime.min.time()))
    end_of_tomorrow = timezone.make_aware(
        datetime.combine(tomorrow, datetime.max.time()))
    bookings = Booking.objects.filter(ticket__session__date__range=(start_of_tomorrow, end_of_tomorrow))
    for booking in bookings:
        ticket = booking.ticket
        ticket.reserved = False
        ticket.save()
        booking.delete()


@shared_task
def send_sessions_reminders():
    # Получить дату следующего дня
    tomorrow = timezone.now() + timedelta(days=1)
    start_of_tomorrow = timezone.make_aware(
        datetime.combine(tomorrow, datetime.min.time()))
    end_of_tomorrow = timezone.make_aware(
        datetime.combine(tomorrow, datetime.max.time()))
    orders = Order.objects.filter(ticket__session__date__range=(start_of_tomorrow, end_of_tomorrow))
    user_orders = defaultdict(list)
    for order in orders:
        user_orders[order.user].append(order)
    for user, user_orders in user_orders.items():
        performances = []
        for order in user_orders:
            performance_name = order.ticket.session.performance.name
            session_date = order.ticket.session.date.strftime('%Y-%m-%d %H:%M')
            performances.append(f'{performance_name} {session_date}')
        performance_list = "\n".join(performances)
        email_body = (
            f'Уважаемый {user.username},\n\n'
            f'Это напоминание, что у вас есть билеты на следующие спектакли:\n\n'
            f'{performance_list}\n\n'
            'Спасибо!'
        )
        send_mail(
            'Напоминание: Ваши предстоящие спектакли',
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )


@shared_task()
def send_bookings_reminders():
    day_after_tomorrow = timezone.now() + timedelta(days=2)
    start_of_tomorrow = timezone.make_aware(
        datetime.combine(day_after_tomorrow, datetime.min.time()))
    end_of_tomorrow = timezone.make_aware(
        datetime.combine(day_after_tomorrow, datetime.max.time()))
    bookings = Booking.objects.filter(ticket__session__date__range=(start_of_tomorrow, end_of_tomorrow))
    user_bookings = defaultdict(list)
    for booking in bookings:
        user_bookings[booking.user].append(booking)
    for user, user_booking in user_bookings.items():
        performances = []
        for booking in user_bookings:
            performance_name = booking.ticket.session.performance.name
            session_date = booking.ticket.session.date.strftime('%Y-%m-%d %H:%M')
            performances.append(f'{performance_name} {session_date}')
        performance_list = "\n".join(performances)
        email_body = (
            f'Уважаемый {user.username},\n\n'
            f'Это напоминание, что у вас есть бронирования билетов на следующие спектакли:\n\n'
            f'{performance_list}\n\n'
            f'Завтра последний день выкупа билетов\n\n'
            'Спасибо!'
        )
        send_mail(
            'Напоминание: Ваши о вашем бронировании билетов',
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )


