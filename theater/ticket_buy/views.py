import json
from datetime import datetime

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views import View
import pdfkit

from poster.models import Session
from theater_info.core_utils import get_navigation_menu
from ticket_buy.hall_scheme_services import hall_scheme
from ticket_buy.models import Booking, Order
from ticket_buy.purchase_services import create_ticket_booking


class TicketBookingView(View):
    """Бронирование билета"""

    def get(self, request, performance_slug, session_pk):
        menu = get_navigation_menu(request.user)
        session = get_object_or_404(Session, id=session_pk)
        seating_chart = hall_scheme(session)
        context = {
            'menu': menu,
            'session': session,
            'seating_chart': seating_chart,
        }
        return render(request, "ticket_buy/ticket_booking.html", context=context)

    def post(self, request, performance_slug, session_pk):
        if request.user.is_authenticated:
            selected_seats_json = request.POST.get('selected_seats')
            selected_seats = json.loads(selected_seats_json)
            for seat in selected_seats:
                if create_ticket_booking(request.user, seat, session_pk):
                    continue
                else:
                    messages.error(request, 'Больше 5 бронирований.')
            return redirect('basket')
        else:
            return redirect('site_login')


class BasketView(View):
    """Козрина бронирований"""

    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            menu = get_navigation_menu(user)
            today = datetime.today()
            bookings = Booking.objects.filter(user=user, ticket__session__date__gte=today)
            context = {
                'menu': menu,
                'booking_list': bookings,
            }
            return render(request, "ticket_buy/basket.html", context=context)
        else:
            return redirect('site_login')

    def post(self, request):
        if request.user.is_authenticated:
            action = request.POST.get('action')
            if action == 'buy':
                self.handle_buy(request)
            elif action.startswith('delete_'):
                booking_id = action.split('_')[1]
                self.handle_delete(request, booking_id)
            return redirect('basket')
        else:
            return redirect('site_login')

    def handle_delete(self, request, booking_id):
        try:
            booking = Booking.objects.get(pk=booking_id, user=request.user)
            booking.delete()
            messages.success(request, 'Билет успешно удален.')
        except Booking.DoesNotExist:
            messages.error(request, 'Билет не найден.')

    def handle_buy(self, request):
        selected_tickets = request.POST.getlist('tickets')
        if selected_tickets:
            bookings = Booking.objects.filter(pk__in=selected_tickets, user=request.user)
            for booking in bookings:
                ticket = booking.ticket
                Order(user=request.user, ticket=ticket).save()
                ticket.reserved = False
                ticket.sold = True
                ticket.save()
                booking.delete()
            messages.success(request, 'Билеты успешно куплены.')
        else:
            messages.error(request, 'Вы не выбрали ни одного билета.')


class OrderView(View):
    """Представление заказанных билетов пользователя"""

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            if 'download' in request.GET:
                return self.generate_pdf(request)
            menu = get_navigation_menu(user)
            today = datetime.today()
            orders = Order.objects.filter(user=user, ticket__session__date__gte=today).order_by('ticket__session__date')
            context = {
                'menu': menu,
                'order_list': orders,
            }
            return render(request, "ticket_buy/user_orders.html", context=context)

    def generate_pdf(self, request):
        if request.user.is_authenticated:
            action = request.GET.get('download')
            if action.startswith('download_'):
                order_pk = action.split('_')[1]
                order = get_object_or_404(Order, pk=order_pk, user=request.user)
                context = {
                    "order": order,
                }
                html_string = render_to_string('ticket_buy/user_order_pdf.html', context)
                pdf = pdfkit.from_string(html_string, False)

                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="ticket.pdf"'
                return response
        else:
            redirect("main_page")



