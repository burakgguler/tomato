from rest_framework.pagination import PageNumberPagination


class RestaurantPagination(PageNumberPagination):
    page_size = 3
