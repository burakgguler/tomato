# Generated by Django 3.2.15 on 2022-09-10 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_auto_20220910_0820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
