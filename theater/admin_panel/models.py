from django.db import models
from django.utils import timezone

from poster.models import Performance


class DailyPerformanceStatistics(models.Model):
    date = models.DateField("Дата", default=timezone.now)
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, verbose_name="Спектакль")
    total_tickets = models.IntegerField("Общее количество билетов")
    sold_tickets = models.IntegerField("Проданные билеты")
    revenue = models.DecimalField("Доход", max_digits=10, decimal_places=2)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return f"{self.performance.name} - {self.date}"


class DailyTimeStatistics(models.Model):
    date = models.DateTimeField("Дата и время", default=timezone.now)
    total_tickets = models.IntegerField("Общее количество билетов")
    sold_tickets = models.IntegerField("Проданные билеты")
    revenue = models.DecimalField("Доход", max_digits=10, decimal_places=2)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return f"{self.date} - {self.sold_tickets}"


