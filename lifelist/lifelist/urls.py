from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from app.views import IndexView, HomeView, RegisterView, LoginView, \
    LogoutView, BucketlistDetailView, AddBucketlistView, \
    EditBucketlistView, DeleteBucketlistView, AddItemView, EditItemView, \
    DeleteItemView

urlpatterns = [
    # Django Admin
    url(r'^admin/', admin.site.urls),
    # API
    url(r'^api/v1/', include('api.urls')),
    # Front-End
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^home', HomeView.as_view(), name='home'),
    url(r'^register$', RegisterView.as_view(), name='register'),
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),
    url(r'^bucketlists/(?P<slug>[-\w]+)/$', BucketlistDetailView.as_view(),
        name='bucketlist-detail'),
    url(r'^add-bucketlist/$', AddBucketlistView.as_view(),
        name='add-bucketlist'),
    url(r'^edit-bucketlist/(?P<pk>\d+)/$', EditBucketlistView.as_view(),
        name='edit-bucketlist'),
    url(r'^delete-bucketlist/(?P<pk>\d+)/$', DeleteBucketlistView.as_view(),
        name='delete-bucketlist'),
    url(r'^add-item/$', AddItemView.as_view(), name='add-item'),
    url(r'^edit-item/(?P<pk>\d+)/$', EditItemView.as_view(), name='edit-item'),
    url(r'^delete-item/(?P<pk>\d+)/$', DeleteItemView.as_view(),
        name='delete-item'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
