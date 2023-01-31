from django.urls import path

from restaurant.api.views import (RestaurantListAPIView,
                                  RestaurantDetailAPIView,
                                  RestaurantUpdateAPIView,
                                  RestaurantCreateAPIView)

app_name = 'restaurant'

urlpatterns = [
    path('list/', RestaurantListAPIView.as_view(), name='list'),
    path('detail/<slug>/', RestaurantDetailAPIView.as_view(), name='detail'),
    path('update/<slug>/', RestaurantUpdateAPIView.as_view(), name='update'),
    path('create/', RestaurantCreateAPIView.as_view(), name='create')
]
