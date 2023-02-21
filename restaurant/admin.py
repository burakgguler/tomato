from django.contrib import admin
from restaurant.models import Cuisine, Restaurant, RestaurantCuisine

admin.site.register(Restaurant)
admin.site.register(Cuisine)
admin.site.register(RestaurantCuisine)
