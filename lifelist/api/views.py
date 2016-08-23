from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, FormView, TemplateView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from rest_framework import viewsets, generics, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from api.models import Bucketlist, Item
from api.forms import RegistrationForm, LoginForm, BucketlistForm, ItemForm
from api.serializers import BucketlistSerializer, ItemSerializer, \
                            UserSerializer
from api.permissions import IsOwnerOrReadOnly


# Front-End Views

class IndexView(TemplateView):
    """
    Handles the index URL
    """
    def get(self, request):
        return render(request, "index.html")


class HomeView(LoginRequiredMixin, TemplateView):
    """
    Handles the dashboard homepage
    """
    login_url = '/'

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


class BucketlistDetailView(LoginRequiredMixin, DetailView):
    """ View to handle display of individual bucket lists """
    login_url = '/'

    def get(self, request, slug):
        bucketlist = get_object_or_404(Bucketlist, slug=slug)
        items = Item.objects.filter(bucketlist=bucketlist)
        context = {'bucketlist': bucketlist, 'items': items}
        return render(request, 'bucketlist.html', context)


class AddBucketlistView(LoginRequiredMixin, View):
    """ View to handle adding a bucket list """
    def post(self, request):
        add_bucketlist_form = BucketlistForm(request.POST, request.FILES)
        if add_bucketlist_form.is_valid():
            bucketlist = add_bucketlist_form.save(commit=False)
            bucketlist.title = request.POST.get('title')
            bucketlist.description = request.POST.get('description')
            bucketlist.image = request.FILES.get('image')
            bucketlist.created_by = request.user
            bucketlist.save()
            return HttpResponseRedirect(reverse('home'))

        context = {'add_bucketlist_form': add_bucketlist_form}
        return render(request, 'dashboard.html', context)


class DeleteBucketlistView(LoginRequiredMixin, DeleteView):
    model = Bucketlist
    success_url = reverse_lazy('home')
    template_name = 'dashboard.html'

    def get_event(self, queryset=None):
        """ Hook to ensure bucket list was created by request.user. """
        bucketlist = super(DeleteBucketlistView, self).get_event()
        if not bucketlist.created_by == self.request.user:
            raise Http404
        return bucketlist

    def get_context_data(self, **kwargs):
        context = super(DeleteBucketlistView, self).get_context_data(**kwargs)
        return context


class EditBucketlistView(UpdateView):
    model = Bucketlist
    form_class = BucketlistForm
    success_url = reverse_lazy('home')
    template_name = 'dashboard.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(EditBucketlistView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EditBucketlistView, self).get_context_data(**kwargs)
        return context


class AddItemView(LoginRequiredMixin, View):
    """ View to handle adding a bucket list """
    def post(self, request):
        add_item_form = ItemForm(request.POST, request.FILES)
        if add_item_form.is_valid():
            item = add_item_form.save(commit=False)
            item.title = request.POST.get('title')
            item.description = request.POST.get('description')
            bucketlist_id = request.POST.get('bucketlist_id')
            item.bucketlist = Bucketlist.objects.get(id=bucketlist_id)
            item.created_by = request.user
            item.save()
            return HttpResponseRedirect(reverse(
                'bucketlist-detail',
                kwargs={'slug': item.bucketlist.slug}))

        context = {'add_item_form': add_item_form}
        return render(request, 'dashboard.html', context)


class EditItemView(UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'bucketlist.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(EditItemView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        item = self.get_object()
        success_url = reverse_lazy(
            'bucketlist-detail', kwargs={'slug': item.bucketlist.slug})
        return success_url

    def get_context_data(self, **kwargs):
        context = super(EditItemView, self).get_context_data(**kwargs)
        return context


class DeleteItemView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = 'bucketlist.html'

    def get_event(self, queryset=None):
        """ Hook to ensure item was created by request.user. """
        bucketlist = super(DeleteItemView, self).get_event()
        if not bucketlist.created_by == self.request.user:
            raise Http404
        return bucketlist

    def get_success_url(self):
        item = self.get_object()
        success_url = reverse_lazy(
            'bucketlist-detail', kwargs={'slug': item.bucketlist.slug})
        return success_url

    def get_context_data(self, **kwargs):
        context = super(DeleteItemView, self).get_context_data(**kwargs)
        return context

# API Views

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
