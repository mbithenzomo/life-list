from django.conf.urls import url, include
from django.contrib import admin
from api.views import IndexView, HomeView, TestView

urlpatterns = [
    # Django Admin
    url(r'^admin/', admin.site.urls),
    # API
    url(r'^api/v1/', include('api.urls')),
    # Front End
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^home', HomeView.as_view(), name='home'),
    url(r'^test', TestView.as_view(), name='test'),
]
