from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'api/tokens', views.TokenViewSet, basename='token')
router.register(r'api/sentences', views.SentenceViewSet, basename='sentence')
router.register(r'api/counts', views.CountViewSet, basename='count')
router.register(r'api/documents', views.DocumentViewSet, basename='document')


urlpatterns = [
    path('', include(router.urls)),
    # path('', views.index, name='index'),
]