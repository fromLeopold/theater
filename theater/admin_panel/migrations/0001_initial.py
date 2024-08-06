# Generated by Django 5.0.4 on 2024-05-26 21:08

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('poster', '0010_alter_session_options_alter_performance_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Дата')),
                ('total_tickets', models.IntegerField(verbose_name='Общее количество билетов')),
                ('sold_tickets', models.IntegerField(verbose_name='Проданные билеты')),
                ('revenue', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Доход')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('performance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poster.performance', verbose_name='Спектакль')),
            ],
        ),
    ]
