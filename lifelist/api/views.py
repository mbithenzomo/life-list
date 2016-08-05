from django.views.generic import TemplateView
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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


class TestView(TemplateView):
    """
    Testing react
    """
    def get(self, request):
        return render(request, 'test.html')


class BucketlistList(generics.ListCreateAPIView):
    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer
    permission_classes = (IsAuthenticated,)


class BucketlistDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer
    permission_classes = (IsAuthenticated,
                          IsOwnerOrReadOnly,)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, pk=None):
        if pk == 'i':
            return Response(UserSerializer(request.user,
                            context={'request': request}).data)
        return super(UserDetail, self).retrieve(request, pk)
