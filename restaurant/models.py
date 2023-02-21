from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from utils.models import StarterModel


class Restaurant(StarterModel):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name="created_restaurants")
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="modified_restaurants")
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True, unique=True, null=False)
    phone = models.IntegerField(null=True)
    opening_time = models.IntegerField(null=True)
    closing_time = models.IntegerField(null=True)

    class Meta:
        ordering = ['-id']

    def get_slug(self):
        slug = slugify(self.name.replace('ı', 'i'))
        unique = slug
        number = 1

        while Restaurant.objects.filter(slug=unique).exists():
            unique = '{}-{}'.format(slug, number)
            number += 1

        return unique

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = self.get_slug()
        return super(Restaurant, self).save(*args, **kwargs)


class Cuisine(StarterModel):
    name = models.CharField(max_length=128, verbose_name=_("Cuisine Name"))


class RestaurantCuisine(StarterModel):
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
