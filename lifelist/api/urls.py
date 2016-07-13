from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^bucketlists/$', views.bucketlist_list),
    url(r'^bucketlists/(?P<pk>[0-9]+)/$', views.bucketlist_detail),
]
