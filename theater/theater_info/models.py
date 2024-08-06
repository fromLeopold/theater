from django.db import models
from transliterate import translit


class SocialMedia(models.Model):
    name = models.CharField("Название", primary_key=True, db_index=True, max_length=50)
    address = models.CharField("Адрес", max_length=50)

    def __str__(self):
        return f'{self.name}: {self.address}'

    class Meta:
        verbose_name = "Социальная сеть"
        verbose_name_plural = "Социальные сети"


class Theater(models.Model):
    name = models.CharField("Название", db_index=True, max_length=50)
    type = models.CharField("Вид театра", max_length=50)
    address = models.CharField("Адрес", max_length=50)
    phone_number = models.CharField('Контактный номер телефона', max_length=20)
    email = models.EmailField("Электронная почта", max_length=254, unique=True)
    social_media = models.ManyToManyField(SocialMedia, verbose_name="Социальные сети", blank=True)

    def __str__(self):
        return f'{self.name}: {self.address}'

    class Meta:
        verbose_name = "Театра"
        verbose_name_plural = "Театры"


class HallSector(models.Model):
    name = models.CharField("Название", primary_key=True, db_index=True, max_length=50)
    description = models.TextField("Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Сектор зала"
        verbose_name_plural = "Секторы зала"


class Hall(models.Model):
    name = models.CharField("Название", db_index=True, max_length=50)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, verbose_name="Театр")
    slug = models.SlugField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        self.slug = (
            translit(self.name, 'ru', reversed=True)
            .replace(" ", '_')
            .replace("'", "")
            .replace(":", "")
            .replace('"', "")
            .replace(".", "")
            .replace(",", ""))
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}: {self.theater.name}'

    class Meta:
        verbose_name = "Зал"
        verbose_name_plural = "Залы"


class Seat(models.Model):
    row = models.PositiveIntegerField("Ряд")
    place = models.PositiveIntegerField("Место")
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, verbose_name="Зал")
    hall_sector = models.ForeignKey(HallSector, on_delete=models.CASCADE, verbose_name="Часть зала")
    standard_price = models.DecimalField("Стандартная цена", max_digits=10, decimal_places=2)
    served = models.BooleanField("Обслуживается", default=True)

    def __str__(self):
        return f'{self.hall}: {self.row}-{self.place}'

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"


class Troupe(models.Model):
    last_name = models.CharField("Фамилия", max_length=50)
    first_name = models.CharField("Имя", max_length=50)
    middle_name = models.CharField("Отчество", max_length=50)
    title = models.CharField("Звание", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField(upload_to='troupe/', verbose_name="Портрет", null=True)
    art_group = models.BooleanField("Художественное руководство", default=False)
    actor = models.BooleanField("Актер", default=False)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    class Meta:
        verbose_name = "Труппа"
        verbose_name_plural = "Труппа"
