# Generated by Django 3.2.15 on 2023-02-25 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0011_auto_20230225_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='closing_time',
            field=models.TimeField(null=True, verbose_name='Closing Time'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='opening_time',
            field=models.TimeField(null=True, verbose_name='Opening Time'),
        ),
    ]
