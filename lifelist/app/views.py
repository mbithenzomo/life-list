from app.forms import RegistrationForm, BucketlistForm, ItemForm
from api.models import Bucketlist, Item
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, TemplateView, DetailView
from django.views.generic.edit import DeleteView, UpdateView


class IndexView(TemplateView):
    """Handles the index URL, which is the authentication page"""

    def get(self, request):
        return render(request, "index.html")


class DashboardView(LoginRequiredMixin, TemplateView):
    """Handles the dashboard homepage"""
    login_url = '/'

    def get(self, request):
        bucketlists = Bucketlist.objects.filter(created_by=request.user)
        return render(request, "dashboard.html", {'bucketlists': bucketlists})


class RegisterView(View):
    """View to handle user registration"""

    def post(self, request):
        register_form = RegistrationForm(request.POST)

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "That email address is already in use.")
        elif register_form.is_valid():
            user = register_form.save(commit=False)
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.set_password(password)
            user.save()
            print user.password
            messages.success(request,
                             "Successfully registered! Login to get started.")
            return HttpResponseRedirect(reverse('index'))
        context = {'register_form': register_form}
        return render(request, 'index.html', context)


class LoginView(View):
    """View to handle user login"""

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        try:
            login(request, user)
            return HttpResponseRedirect(reverse('dashboard'))
        except:
            messages.error(request,
                           "Incorrect username or password! Please try again.")
            return render(request, 'index.html')


class LogoutView(View):
    """View to handle user logout"""

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class BucketlistDetailView(LoginRequiredMixin, DetailView):
    """View to handle display of individual bucket list"""
    login_url = '/'

    def get(self, request, slug):
        bucketlist = get_object_or_404(Bucketlist, slug=slug)
        items = Item.objects.filter(item_bucketlist=bucketlist)
        context = {'bucketlist': bucketlist, 'items': items}
        return render(request, 'bucketlist.html', context)


class AddBucketlistView(LoginRequiredMixin, View):
    """View to handle adding a bucket list"""

    def post(self, request):
        add_bucketlist_form = BucketlistForm(request.POST, request.FILES)
        if add_bucketlist_form.is_valid():
            bucketlist = add_bucketlist_form.save(commit=False)
            bucketlist.title = request.POST.get('title')
            bucketlist.description = request.POST.get('description')
            bucketlist.image = request.FILES.get('image')
            bucketlist.created_by = request.user
            bucketlist.save()
            return HttpResponseRedirect(reverse('dashboard'))
        context = {'add_bucketlist_form': add_bucketlist_form}
        return render(request, 'dashboard.html', context)


class DeleteBucketlistView(LoginRequiredMixin, DeleteView):
    """View to handle deleting a bucket list"""
    model = Bucketlist
    success_url = reverse_lazy('dashboard')
    template_name = 'dashboard.html'

    def get_event(self, queryset=None):
        """Hook to ensure bucket list was created by request.user """
        bucketlist = super(DeleteBucketlistView, self).get_event()
        if not bucketlist.created_by == self.request.user:
            raise Http404
        return bucketlist

    def get_context_data(self, **kwargs):
        context = super(DeleteBucketlistView, self).get_context_data(**kwargs)
        return context


class EditBucketlistView(UpdateView):
    """View to handle editing a bucket list"""
    model = Bucketlist
    form_class = BucketlistForm
    success_url = reverse_lazy('dashboard')
    template_name = 'bucketlist.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(EditBucketlistView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EditBucketlistView, self).get_context_data(**kwargs)
        return context


class AddItemView(LoginRequiredMixin, View):
    """View to handle adding a bucket list item"""

    def post(self, request):
        add_item_form = ItemForm(request.POST, request.FILES)
        if add_item_form.is_valid():
            item = add_item_form.save(commit=False)
            item.title = request.POST.get('title')
            item.description = request.POST.get('description')
            bucketlist_id = request.POST.get('bucketlist_id')
            item.item_bucketlist = Bucketlist.objects.get(id=bucketlist_id)
            item.save()
            return HttpResponseRedirect(reverse(
                'bucketlist-detail',
                kwargs={'slug': item.item_bucketlist.slug}))

        context = {'add_item_form': add_item_form}
        return render(request, 'dashboard.html', context)


class EditItemView(UpdateView):
    """View to handle editing a bucket list item"""
    model = Item
    form_class = ItemForm
    template_name = 'bucketlist.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(EditItemView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        item = self.get_object()
        success_url = reverse_lazy(
            'bucketlist-detail', kwargs={'slug': item.item_bucketlist.slug})
        return success_url

    def get_context_data(self, **kwargs):
        context = super(EditItemView, self).get_context_data(**kwargs)
        return context


class DeleteItemView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = 'bucketlist.html'

    def get_event(self, queryset=None):
        """Hook to ensure item was created by request.user"""
        bucketlist = super(DeleteItemView, self).get_event()
        if not bucketlist.created_by == self.request.user:
            raise Http404
        return bucketlist

    def get_success_url(self):
        item = self.get_object()
        success_url = reverse_lazy(
            'bucketlist-detail', kwargs={'slug': item.item_bucketlist.slug})
        return success_url

    def get_context_data(self, **kwargs):
        context = super(DeleteItemView, self).get_context_data(**kwargs)
        return context
