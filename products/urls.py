from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, upload_json
from django.urls import path
router = DefaultRouter()
router.register(r'', ProductViewSet, basename='product')

urlpatterns = [
    path('upload/', upload_json),
    *router.urls,
]
