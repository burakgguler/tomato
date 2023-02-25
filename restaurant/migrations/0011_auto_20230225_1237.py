# Generated by Django 3.2.15 on 2023-02-25 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0010_alter_restaurant_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='cuisines',
            field=models.ManyToManyField(related_name='restaurants', to='restaurant.Cuisine', verbose_name='Cuisines'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='tags',
            field=models.ManyToManyField(related_name='restaurants', to='restaurant.Tag', verbose_name='Tags'),
        ),
        migrations.DeleteModel(
            name='RestaurantCuisine',
        ),
    ]
