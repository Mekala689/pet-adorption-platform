from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
# Add API viewsets here when needed

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', api_views.stats_api, name='stats_api'),
]
