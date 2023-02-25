from django.contrib import admin
from restaurant.models import Cuisine, Restaurant, Tag, Feature


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'opening_time', 'closing_time', 'average_price')
    list_filter = ('tags', 'cuisines', 'features')
    exclude = ('slug',)


@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('caption',)


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name',)
