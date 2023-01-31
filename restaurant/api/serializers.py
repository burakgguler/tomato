from rest_framework import serializers

from restaurant.models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    """
    url = serializers.HyperlinkedIdentityField(
        view_name='restaurant:detail',
        lookup_field='slug'
    )
    """
    username = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = [
            'username',
            'modified_by',
            'name',
            'cuisine',
            'phone',
            'slug',  # url
            'created_date',
            'modified_date'
        ]

    def get_username(self, obj):
        return str(obj.created_by.username)


class RestaurantCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            'name',
            'cuisine',
            'phone'
        ]

    # def validate(self, attrs):
    #    if attrs['cuisine'] == "burakk":
    #        raise serializers.ValidationError('olmazzzz')
    #    return attrs
