from django.views.generic import TemplateView
from django.shortcuts import render
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from api.models import Bucketlist
from api.serializers import BucketlistSerializer, UserSerializer
from api.permissions import IsOwnerOrReadOnly


class IndexView(TemplateView):
    """
    Handles the index URL
    """
    def get(self, request):
        return render(request, 'index.html')


class HomeView(TemplateView):
    """
    Handles the dashboard homepage
    """
    def get(self, request):
        return render(request, 'dashboard.html')


class BucketlistList(generics.ListCreateAPIView):
    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class BucketlistDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
