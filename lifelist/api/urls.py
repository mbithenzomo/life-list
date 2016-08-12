from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as authviews
from api import views

router = DefaultRouter()
router.register(r'bucketlists', views.BucketlistViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/login/', authviews.obtain_auth_token),
]
