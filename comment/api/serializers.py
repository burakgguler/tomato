from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from comment.models import Comment
from restaurant.models import Restaurant


class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['user', 'created_date', 'modified_date']

    def validate(self, attrs):
        if attrs["parent"]:
            if attrs["parent"].restaurant != attrs["restaurant"]:
                raise serializers.ValidationError("parent error!")

        return attrs


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']


class RestaurantCommentSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'slug']


class CommentListSerializer(ModelSerializer):
    replies = SerializerMethodField()
    user = UserSerializer()
    restaurant = RestaurantCommentSerializer()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_replies(self, obj):
        if obj.any_replies:
            return CommentListSerializer(obj.get_replies(), many=True).data


class CommentDeleteUpdateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']
