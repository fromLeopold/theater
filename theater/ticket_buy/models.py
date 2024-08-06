import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from poster.models import Ticket


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, verbose_name="Пользователь")
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, editable=False, verbose_name="Билет")
    date_time = models.DateTimeField("Дата и время бронирования", editable=False, default=timezone.now)
    booking_number = models.CharField(max_length=20, unique=True, editable=False, default='')

    def save(self, *args, **kwargs):
        if not self.booking_number:
            self.booking_number = self.generate_booking_number()
        super().save(*args, **kwargs)

    def generate_booking_number(self):
        return str(uuid.uuid4()).split('-')[0]

    def __str__(self):
        return self.ticket.session.performance.name

    class Meta:
        verbose_name = "Бронь"
        verbose_name_plural = "Брони"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, verbose_name="Пользователь")
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, editable=False, verbose_name="Билет")
    date_time = models.DateTimeField("Дата и время заказа", editable=False, default=timezone.now)
    order_number = models.CharField(max_length=20, unique=True, editable=False, default='')

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    def generate_order_number(self):
        return str(uuid.uuid4()).split('-')[0]

    def __str__(self):
        return self.ticket.session.performance.name

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
