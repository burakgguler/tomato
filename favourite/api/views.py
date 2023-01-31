from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from favourite.api.paginations import FavouritePagination
from favourite.api.permissions import IsCreator
from favourite.api.serializers import FavouriteListCreateSerializer, FavouriteRetrieveUpdateSerializer
from favourite.models import Favourite


class FavouriteListCreateAPIView(ListCreateAPIView):
    serializer_class = FavouriteListCreateSerializer
    pagination_class = FavouritePagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavouriteRetrieveUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteRetrieveUpdateSerializer
    lookup_field = 'pk'
    permission_classes = [IsCreator]
