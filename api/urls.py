from django.urls import include, path
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register(r'invoices', InvoiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth_rest/', include('rest_framework.urls', namespace='rest_framework')),
]