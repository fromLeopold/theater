# Generated by Django 5.0.4 on 2024-05-09 10:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theater_info', '0005_seat_served'),
    ]

    operations = [
        migrations.CreateModel(
            name='Social_media',
            fields=[
                ('name', models.CharField(db_index=True, max_length=50, primary_key=True, serialize=False, verbose_name='Название')),
                ('address', models.CharField(max_length=50, verbose_name='Адрес')),
            ],
            options={
                'verbose_name': 'Социальная сеть',
                'verbose_name_plural': 'Социальные сети',
            },
        ),
        migrations.AddField(
            model_name='theater',
            name='social_media',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='theater_info.social_media', verbose_name='Социальные сети'),
        ),
    ]
