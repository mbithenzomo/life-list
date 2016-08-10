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
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticated,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    """
    Viewset prividing `list`, `create` and `retrieve`
    actions for User objects.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        data = request.data
        username = data.get("username")
        password, confirm_password = data.get("password"),\
            data.get("confirm_password")
        if not confirm_password:
            return Response({"error": "You must confirm your password."},
                            status=status.HTTP_400_BAD_REQUEST)
        if password == confirm_password:
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                user = self.get_object()
                user.set_password(data['password'])
                user.save()
                serializer.save(username=username)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "The passwords do not match."},
                            status=status.HTTP_400_BAD_REQUEST)

    @list_route()
    def recent_users(self, request):
        recent_users = User.objects.all().order("-date_created")

        page = self.paginate_queryset(recent_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)
