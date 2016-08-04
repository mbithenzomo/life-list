from django.conf.urls import url, include
from api.views import IndexView, HomeView, BucketlistList, \
                      BucketlistDetail, UserList, UserDetail
from api import views

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^home', HomeView.as_view(), name='home'),
    url(r'^bucketlists/$', views.BucketlistList.as_view()),
    url(r'^bucketlists/(?P<pk>[0-9]+)/$', views.BucketlistDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^auth/', include('rest_framework.urls',
                           namespace='rest_framework')),
]
