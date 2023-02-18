from django.contrib.auth.models import User
from django.db import models

from restaurant.models import Restaurant


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    content = models.CharField(max_length=120, null=True, blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.user.username
