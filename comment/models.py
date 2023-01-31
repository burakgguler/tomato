from django.contrib.auth.models import User
from django.db import models

from restaurant.models import Restaurant
from utils.models import StarterModel


class Comment(StarterModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        ordering = ('created_date', )

    def __str__(self):
        return self.restaurant.name + " " + self.user.username

    def get_replies(self):
        return Comment.objects.filter(parent=self)

    @property
    def any_replies(self):
        return Comment.objects.filter(parent=self).exists()
