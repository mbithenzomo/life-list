from rest_framework import serializers
from api.models import Bucketlist, Item
from django.contrib.auth.models import User


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ("id", "bucketlist", "created_by", "title", "description",
                  "date_created", "date_modified", "is_done")


class BucketlistSerializer(serializers.ModelSerializer):

    items = ItemSerializer(many=True)

    class Meta:
        model = Bucketlist
        fields = ("id", "created_by", "title", "description",
                  "items", "date_created", "date_modified")


class UserSerializer(serializers.ModelSerializer):
    bucketlists = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title')

    password = serializers.CharField(max_length=100,
                                     style={'input_type': 'password'},
                                     required=True, write_only=True)

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ("id", "username", "password", "bucketlists")
