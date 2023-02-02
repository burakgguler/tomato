# Generated by Django 3.2.15 on 2022-09-10 08:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='closing_time',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='opening_time',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='phone',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]