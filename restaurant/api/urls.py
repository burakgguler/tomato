from django.urls import path
from django.views.decorators.cache import cache_page

from restaurant.api.views import (RestaurantListAPIView,
                                  RestaurantDetailAPIView,
                                  RestaurantUpdateAPIView,
                                  RestaurantCreateAPIView)

app_name = 'restaurant'

urlpatterns = [
    path('list/', cache_page(60 * 1)(RestaurantListAPIView.as_view()), name='list'),
    path('detail/<slug>/', RestaurantDetailAPIView.as_view(), name='detail'),
    path('update/<slug>/', RestaurantUpdateAPIView.as_view(), name='update'),
    path('create/', RestaurantCreateAPIView.as_view(), name='create')
]
