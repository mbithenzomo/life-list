from api.models import Bucketlist, Item
from api.permissions import IsOwnerOrReadOnlyBucketlist, IsOwnerOrReadOnlyItem
from api.serializers import BucketlistSerializer, ItemSerializer, \
                            UserSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class BucketlistViewSet(viewsets.ModelViewSet):
    """
    Viewset providing `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Bucketlist objects.
    URL: /api/v1/bucketlists/
    """
    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer
    permission_classes = (IsAuthenticated,
                          IsOwnerOrReadOnlyBucketlist,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ItemViewSet(viewsets.ModelViewSet):
    """
    Viewset providing `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Item objects.
    URL: /api/v1/bucketlists/<pk>/items/
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticated,
                          IsOwnerOrReadOnlyItem,)

    def perform_create(self, serializer):
        item_bucketlist_id = self.kwargs.get("bucketlist_pk")
        serializer.save(item_bucketlist_id=item_bucketlist_id)


class UserViewSet(viewsets.ModelViewSet):
    """
    Viewset providing `list`, `create` and `retrieve`
    actions for User objects.
    URL: /api/v1/users/
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
