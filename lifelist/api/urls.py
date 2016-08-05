from django.conf.urls import url, include
from rest_framework.authtoken import views as authviews
from api.views import IndexView, HomeView, Bucketlists, \
                      Bucketlist, Users, User, TestView
from api import views

urlpatterns = [
    url(r'^bucketlists/$', views.Bucketlists.as_view()),
    url(r'^bucketlists/(?P<pk>[0-9]+)/$', views.Bucketlist.as_view()),
    url(r'^bucketlists/(?P<bucketlist_pk>[0-9]+)/items/$', views.Items.as_view()),
    url(r'^bucketlists/(?P<bucketlist_pk>[0-9]+)/items/(?P<item_pk>[0-9]+)/$', views.Item.as_view()),
    url(r'^users/$', views.Users.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.User.as_view()),
    url(r'^auth/login/', authviews.obtain_auth_token),
]
