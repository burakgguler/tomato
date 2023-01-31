from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from favourite.models import Favourite


class FavouriteListCreateSerializer(ModelSerializer):
    class Meta:
        model = Favourite
        fields = '__all__'

    def validate(self, attrs):
        queryset = Favourite.objects.filter(restaurant=attrs["restaurant"], user=attrs["user"])
        if queryset.exists():
            raise serializers.ValidationError("You already added this restaurant to favourites!")

        return attrs


class FavouriteRetrieveUpdateSerializer(ModelSerializer):
    class Meta:
        model = Favourite
        fields = ['content']
