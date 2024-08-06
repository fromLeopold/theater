# Generated by Django 5.0.4 on 2024-05-08 10:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Зал',
                'verbose_name_plural': 'Залы',
            },
        ),
        migrations.CreateModel(
            name='Hall_part',
            fields=[
                ('name', models.CharField(db_index=True, max_length=50, primary_key=True, serialize=False, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('standard_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стандартная цена')),
            ],
            options={
                'verbose_name': 'Часть зала',
                'verbose_name_plural': 'Части зала',
            },
        ),
        migrations.CreateModel(
            name='Theater',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, verbose_name='Название')),
                ('type', models.CharField(max_length=50, verbose_name='Вид театра')),
                ('address', models.CharField(max_length=50, verbose_name='Адрес')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Контактный номер телефона')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Электронная почта')),
            ],
            options={
                'verbose_name': 'Контакты театра',
                'verbose_name_plural': 'Контакты театров',
            },
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.PositiveIntegerField(verbose_name='Ряд')),
                ('place', models.PositiveIntegerField(verbose_name='Место')),
                ('hall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='theater_info.hall', verbose_name='Зал')),
                ('hall_part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='theater_info.hall_part', verbose_name='Часть зала')),
            ],
            options={
                'verbose_name': 'Место',
                'verbose_name_plural': 'Места',
            },
        ),
        migrations.AddField(
            model_name='hall',
            name='theater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='theater_info.theater', verbose_name='Театр'),
        ),
    ]
