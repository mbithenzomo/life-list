from rest_framework import serializers
from api.models import Bucketlist
from django.contrib.auth.models import User


class BucketlistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bucketlist
        fields = ("id", "created_by", "title", "description",
                  "date_created", "date_modified")


class UserSerializer(serializers.ModelSerializer):
    bucketlists = serializers.PrimaryKeyRelatedField(
                    many=True,
                    queryset=Bucketlist.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'bucketlists')
