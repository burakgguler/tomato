from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.models import StarterModel


class AbstractLocation(StarterModel):
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=128, verbose_name=_("Official Name"))

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Country(AbstractLocation):
    code = models.CharField(max_length=3, verbose_name=_("Country Code"), unique=True)


class City(AbstractLocation):
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    province_code = models.CharField(max_length=128, verbose_name=_("Province Code"), null=True, blank=True)
    priority = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = (("country", "name"),)


class Township(AbstractLocation):
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    postcode = models.CharField(max_length=128, verbose_name=_("Post/Zip Code"), null=True, blank=True)

    class Meta:
        unique_together = (("city", "name"),)


class District(AbstractLocation):
    township = models.ForeignKey(Township, on_delete=models.PROTECT)
    postcode = models.CharField(max_length=128, verbose_name=_("Post/Zip Code"), null=True, blank=True)

    class Meta:
        unique_together = (("township", "name"),)
