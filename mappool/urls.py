from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register('maps', views.MapViewSet)
router.register('map_pool', views.MapPoolViewSet, base_name='map_pool')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
