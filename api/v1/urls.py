from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FragabiUserViewSet, QuizViewSet, ConsultationViewSet

router = DefaultRouter()
router.register(r'users', FragabiUserViewSet)
router.register(r'assignments', QuizViewSet)
router.register(r'consultations', ConsultationViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
]
