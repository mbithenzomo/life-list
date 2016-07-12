from rest_framework import serializers
from api.models import Bucketlist


class BucketlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bucketlist
        fields = ("id", "created_by", "title", "description",
                  "date_created", "date_modified")
