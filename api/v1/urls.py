from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FragabiUserViewSet

router = DefaultRouter()
router.register(r'users', FragabiUserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
