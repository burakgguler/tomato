from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (ListAPIView,
                                     RetrieveAPIView,
                                     RetrieveUpdateAPIView,
                                     DestroyAPIView,
                                     CreateAPIView)
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser
)

from restaurant.api.paginations import RestaurantPagination
from restaurant.api.permissions import IsCreator
from restaurant.api.serializers import RestaurantSerializer, RestaurantCreateUpdateSerializer
from restaurant.models import Restaurant


class RestaurantListAPIView(ListAPIView):
    serializer_class = RestaurantSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['cuisine']
    pagination_class = RestaurantPagination

    def get_queryset(self):
        queryset = Restaurant.objects.all()

        return queryset


class RestaurantDetailAPIView(RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    lookup_field = 'slug'


class RestaurantUpdateAPIView(RetrieveUpdateAPIView, DestroyModelMixin):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantCreateUpdateSerializer
    lookup_field = 'slug'
    permission_classes = [IsCreator]

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class RestaurantCreateAPIView(CreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
