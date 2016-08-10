from django.conf.urls import url, include
from rest_framework import renderers
from rest_framework.authtoken import views as authviews
from api.views import IndexView, HomeView, BucketlistViewSet, \
                      UserViewSet, TestView
from api import views

bucketlists = BucketlistViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
bucketlist = BucketlistViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
users = UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
user = UserViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = [
    url(r'^bucketlists/$', bucketlists, name='bucketlists'),
    url(r'^bucketlists/(?P<pk>[0-9]+)/$', bucketlist, name='bucketlist'),
    url(r'^users/$', users, name='users'),
    url(r'^users/(?P<pk>[0-9]+)/$', user, name='user'),
    url(r'^auth/login/', authviews.obtain_auth_token),
]
