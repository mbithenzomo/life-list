from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView
from api.views import IndexView, HomeView, RegisterView, LoginView, LogoutView

urlpatterns = [
    # Django Admin
    url(r'^admin/', admin.site.urls),
    # API
    url(r'^api/v1/', include('api.urls')),
    # Front End
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^home', HomeView.as_view(), name='home'),
    url(r'^register$', RegisterView.as_view(), name='register'),
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
