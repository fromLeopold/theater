from django.urls import path

from ticket_buy import views

urlpatterns = [
    path('basket/', views.BasketView.as_view(), name='basket'),
    path('orders/', views.OrderView.as_view(), name='order'),
    path('orders/download/', views.OrderView.as_view(), name='order_download'),
    path('booking/<slug:performance_slug>/<int:session_pk>/', views.TicketBookingView.as_view(), name='ticket_booking'),
]
