from rest_framework import serializers
from api.models import Bucketlist, Item
from django.contrib.auth.models import User


class BucketlistSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(
            many=True,
            queryset=Item.objects.all())

    class Meta:
        model = Bucketlist
        fields = ("id", "created_by", "title", "description",
                  "items", "date_created", "date_modified")


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ("id", "bucketlist", "created_by", "title", "description",
                  "date_created", "date_modified", "is_done")


class UserSerializer(serializers.ModelSerializer):
    bucketlists = serializers.PrimaryKeyRelatedField(
                  many=True,
                  queryset=Bucketlist.objects.all())

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
