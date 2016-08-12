from django.views.generic import TemplateView
from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from api.models import Bucketlist, Item
from api.serializers import BucketlistSerializer, ItemSerializer, \
                            UserSerializer
from api.permissions import IsOwnerOrReadOnly


class IndexView(TemplateView):
    """
    Handles the index URL
    """
    def get(self, request):
        return render(request, "index.html")


class HomeView(TemplateView):
    """
    Handles the dashboard homepage
    """
    def get(self, request):
        return render(request, "dashboard.html")


class TestView(TemplateView):
    """
    Testing react
    """
    def get(self, request):
        return render(request, "test.html")


class BucketlistViewSet(viewsets.ModelViewSet):
    """
    Viewset providing `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Bucketlist objects.
    URL: /api/v1/bucketlists/
    """
    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer
    permission_classes = (IsAuthenticated,
                          IsOwnerOrReadOnly,)

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
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        bucketlist_id = self.kwargs.get("bucketlist_pk")
        serializer.save(created_by=self.request.user,
                        bucketlist_id=bucketlist_id)

    # def perform_create(self, serializer):
    #     bucketlist_id = self.kwargs.get("bucketlist_pk")
    #     bucketlists = Bucketlist.objects.all()
    #     bucketlist = get_object_or_404(bucketlists, id=bucketlist_id)
    #     if bucketlist:
    #         serializer.save(created_by=self.request.user,
    #                         bucketlist_id=bucketlist_id)


class UserViewSet(viewsets.ModelViewSet):
    """
    Viewset providing `list`, `create` and `retrieve`
    actions for User objects.
    URL: /api/v1/users/
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
