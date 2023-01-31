from django.urls import path

from favourite.api.views import FavouriteListCreateAPIView, FavouriteRetrieveUpdateAPIView

app_name = 'favourite'
urlpatterns = [
    path('list-create/', FavouriteListCreateAPIView.as_view(), name='list-create'),
    path('update-delete/<pk>', FavouriteRetrieveUpdateAPIView.as_view(), name='update-delete')
]
