# Generated by Django 5.0.4 on 2024-05-08 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theater_info', '0002_rename_hall_part_hall_sector_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hall_sector',
            options={'verbose_name': 'Сектор зала', 'verbose_name_plural': 'Секторы зала'},
        ),
        migrations.RemoveField(
            model_name='hall_sector',
            name='standard_price',
        ),
        migrations.AddField(
            model_name='seat',
            name='standard_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Стандартная цена'),
            preserve_default=False,
        ),
    ]
