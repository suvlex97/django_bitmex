from django.urls import path, include
from rest_framework import routers

from .views import OrderViewSet

router = routers.SimpleRouter()

router.register(r'orders/(?P<account_name>[^/]+)', OrderViewSet, basename='orders')


urlpatterns = [
    path('', include(router.urls)),
]
