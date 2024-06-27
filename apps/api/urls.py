from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import user

router = DefaultRouter()

router.register(r'user', user.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
