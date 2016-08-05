from django.conf.urls import url, include
from rest_framework.authtoken import views as authviews
from api.views import IndexView, HomeView, BucketlistList, \
                      BucketlistDetail, UserList, UserDetail, TestView
from api import views

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^home', HomeView.as_view(), name='home'),
    url(r'^test', TestView.as_view(), name='test'),
    url(r'^bucketlists/$', views.BucketlistList.as_view()),
    url(r'^bucketlists/(?P<pk>[0-9]+)/$', views.BucketlistDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^auth/login/', authviews.obtain_auth_token),
]
