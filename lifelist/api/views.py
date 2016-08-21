from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import viewsets, generics, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from api.models import Bucketlist, Item
from api.forms import RegistrationForm, LoginForm
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
        bucketlists = Bucketlist.objects.filter(created_by=request.user)
        return render(request, "dashboard.html", {'bucketlists': bucketlists})


class RegisterView(View):
    """ View to handle user registration """
    def post(self, request):
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.password = request.POST.get('password')
            user.save()
            message = "Succesfully registered."
            return HttpResponseRedirect(reverse('index'))
            context = {'message': message, 'user': user}
        else:
            context = {}

        more_context = {'register_form': register_form}
        context.update(more_context)
        return render(request, 'index.html', context)


class LoginView(View):
    """ View to handle user login """
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        try:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        except:
            error = "Incorrect username or password! Please try again."
            context = {'error': error}
            return render(request, 'index.html', context)


class LogoutView(View):
    """ View to handle user logout """
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


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


class UserViewSet(viewsets.ModelViewSet):
    """
    Viewset providing `list`, `create` and `retrieve`
    actions for User objects.
    URL: /api/v1/users/
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
