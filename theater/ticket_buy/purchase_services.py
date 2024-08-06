from django.shortcuts import get_object_or_404

from poster.models import Session, Ticket
from theater_info.models import Seat
from ticket_buy.models import Booking


def create_ticket_booking(user, seat, session_pk):
    """
    Создает бронирование билета.

    :params: user, seat, session_pk
    :return: bool
    """

    session = get_object_or_404(Session, id=session_pk)
    hall = session.hall
    if Booking.objects.filter(user=user).count() < 5:
        sector = seat['sector']
        row = seat['row']
        place = seat['place']
        seat = get_object_or_404(Seat, hall_sector__name=sector, row=row, place=place, hall=hall)
        ticket = get_object_or_404(Ticket, seat=seat, session=session)
        Booking(user=user, ticket=ticket).save()
        ticket.reserved = True
        ticket.save()
        return True
    else:
        return False


