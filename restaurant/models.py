from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError

from utils.models import StarterModel


class Restaurant(StarterModel):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1,
                                   verbose_name=_("Created By"), related_name="created_restaurants")
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                    verbose_name=_("Modified By"), related_name="modified_restaurants")
    tags = models.ManyToManyField("restaurant.Tag", related_name="restaurants", verbose_name=_("Tags"))
    features = models.ManyToManyField("restaurant.Feature", related_name="restaurants", verbose_name=_("Features"))
    cuisines = models.ManyToManyField("restaurant.Cuisine", related_name="restaurants", verbose_name=_("Cuisines"))
    name = models.CharField(max_length=120, verbose_name=_("Restaurant Name"))
    location = models.CharField(max_length=255, verbose_name=_("Location"))
    slug = models.SlugField(db_index=True, unique=True, null=False, verbose_name=_("Slug"))
    phone = models.IntegerField(null=True, verbose_name=_("Phone Number"))
    opening_time = models.TimeField(null=True, verbose_name=_("Opening Time"))
    closing_time = models.TimeField(null=True, verbose_name=_("Closing Time"))
    rating = models.DecimalField(max_digits=3, decimal_places=2, verbose_name=_("Rating"),
                                 validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    average_price = models.IntegerField(verbose_name=_("Average Price"), null=True, blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name

    def get_slug(self):
        slug = slugify(self.name.replace('ı', 'i'))
        unique = slug
        number = 1

        while Restaurant.objects.filter(slug=unique).exists():
            unique = '{}-{}'.format(slug, number)
            number += 1

        return unique

    def validate_times(self):
        if self.closing_time <= self.opening_time:
            raise ValidationError(detail=_("Closing time cannot be earlier than the opening time."))

    def save(self, *args, **kwargs):
        self.slug = self.get_slug()
        self.validate_times()

        return super(Restaurant, self).save(*args, **kwargs)


class Feature(StarterModel):
    name = models.CharField(max_length=256, verbose_name=_("Restaurant Feature"))

    def __str__(self):
        return self.name


class Tag(StarterModel):
    caption = models.CharField(max_length=30, verbose_name=_("Caption"))

    def __str__(self):
        return self.caption


class Cuisine(StarterModel):
    name = models.CharField(max_length=128, verbose_name=_("Cuisine Name"))

    def __str__(self):
        return self.name
