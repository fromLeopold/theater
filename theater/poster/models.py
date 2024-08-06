from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse
from transliterate import translit

from theater_info.models import Hall, Seat


class Genre(models.Model):
    name = models.CharField("Название", primary_key=True, db_index=True, max_length=50)
    description = models.TextField("Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Position(models.Model):
    position = models.CharField("Обязанность в спектакле", max_length=100)
    description = models.TextField("Описание")

    def __str__(self):
        return self.position

    class Meta:
        verbose_name = "Обязанность в спектакле"
        verbose_name_plural = "Обязанности в спектактях"


class PositionExecutorLink(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name="Обязанность в спектакле")
    executor = models.TextField("Исполнитель", max_length=200)

    def __str__(self):
        return f'{self.position}: {self.executor}'

    class Meta:
        verbose_name = "Обязанность-исполнитель"
        verbose_name_plural = "Обязанности-исполнители"


class Role(models.Model):
    role_name = models.CharField("Название роли", max_length=100)
    actor = models.TextField("Актёр", max_length=200)

    def __str__(self):
        return f'{self.role_name}: {self.actor}'

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"


class Performance(models.Model):
    name = models.CharField("Название", max_length=50, db_index=True)
    genre = models.ManyToManyField(Genre, verbose_name="Жанр")
    art_group = models.ManyToManyField(PositionExecutorLink, verbose_name="Художественная группа",
                                       related_name='performances_as_art_group')
    roles = models.TextField("Роли")
    description = models.TextField("Описание")
    poster = models.ImageField(upload_to='performances/', verbose_name="Постер")
    premiere = models.BooleanField("Премьера", default=False)
    duration = models.DurationField("Продолжительность")
    start_date = models.DateField("Дата начала")
    expiration_date = models.DateField("Дата окончания")
    repertoire = models.BooleanField("В репертуаре", default=False)
    url = models.SlugField(max_length=50, unique=True, default='')
    age_restrictions = models.IntegerField(default=12, help_text="Age restriction in years (e.g.,0, 6, 12, 16, 18)")

    def save(self, *args, **kwargs):
        self.url = (
            translit(self.name, 'ru', reversed=True)
            .replace(" ", '-')
            .replace("'", "")
            .replace(":", "")
            .replace('"', "")
            .replace(".", "")
            .replace(",", ""))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('performance_sessions', kwargs={"slug": self.url})

    class Meta:
        verbose_name = "Спектакль"
        verbose_name_plural = "Спектакли"


class Session(models.Model):
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, verbose_name="Спектакль")
    date = models.DateTimeField("Дата и время")
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, verbose_name="Зал")
    price_percentage_increase = models.IntegerField("Процентное увеличение цены",
                                                    validators=[MaxValueValidator(9999), ],
                                                    help_text="Укажите процентное увеличение цены(например 10)",
                                                    default=0)

    def clean(self):
        if Session.objects.filter(date=self.date, hall=self.hall).exists():
            raise ValidationError("На это время уже есть сеанс")

    def save(self, *args, **kwargs):
        if Session.objects.filter(date=self.date, hall=self.hall).exists():
            return super(Session, self).clean()
        else:
            super().save(*args, **kwargs)
            seats = Seat.objects.filter(hall=self.hall)
            for seat in seats:
                ticket = Ticket(seat=seat,
                                session=self,
                                price=seat.standard_price * self.price_percentage_increase + seat.standard_price)
                ticket.save()

    def __str__(self):
        return f'{self.performance}: {self.date}'

    class Meta:
        verbose_name = "Сеанс"
        verbose_name_plural = "Сеансы"
        ordering = ('-date',)


class Ticket(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name="Сеанс")
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, verbose_name="Сиденье")
    sold = models.BooleanField("Продан", default=False)
    reserved = models.BooleanField("Забронирован", default=False)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)

    def __str__(self):
        return self.session.performance.name

    class Meta:
        verbose_name = "Билет"
        verbose_name_plural = "Билеты"
