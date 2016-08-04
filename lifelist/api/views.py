from django.views.generic import TemplateView
from django.shortcuts import render
from rest_framework import generics
from api.models import Bucketlist
from api.serializers import BucketlistSerializer


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


class BucketlistDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer
