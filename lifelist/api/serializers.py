from api.models import Bucketlist, Item
from django.contrib.auth.models import User
from rest_framework import serializers


class ItemSerializer(serializers.ModelSerializer):

    bucketlist = serializers.StringRelatedField(
        read_only=True)

    created_by = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')

    date_created = serializers.DateTimeField(
        format='%d.%m.%Y %H:%M',
        required=False,
        read_only=True)

    date_modified = serializers.DateTimeField(
        format='%d.%m.%Y %H:%M',
        required=False)

    class Meta:
        model = Item
        fields = ("id", "bucketlist", "created_by", "title", "description",
                  "date_created", "date_modified", "is_done")


class BucketlistSerializer(serializers.ModelSerializer):

    created_by = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')

    items = ItemSerializer(
        many=True,
        read_only=True)

    date_created = serializers.DateTimeField(
        format='%d.%m.%Y %H:%M',
        required=False,
        read_only=True)

    date_modified = serializers.DateTimeField(
        format='%d.%m.%Y %H:%M',
        required=False)

    class Meta:
        model = Bucketlist
        fields = ("id", "created_by", "title", "description",
                  "items", "date_created", "date_modified")


class UserSerializer(serializers.ModelSerializer):
    bucketlists = serializers.StringRelatedField(
        read_only=True,
        many=True)

    email = serializers.EmailField(
        max_length=None,
        min_length=None,
        allow_blank=False)

    password = serializers.CharField(
        max_length=100,
        style={'input_type': 'password'},
        required=True,
        write_only=True)

    def create(self, validated_data):
        user = User(username=validated_data['username'],
                    email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "bucketlists")
