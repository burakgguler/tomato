# Generated by Django 3.2.15 on 2023-02-25 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0009_auto_20230225_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='tags',
            field=models.ManyToManyField(related_name='restaurants', to='restaurant.Tag'),
        ),
    ]
