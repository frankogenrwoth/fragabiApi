from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter
from .views import FragabiUserViewSet, QuizViewSet, ConsultationViewSet


class CSRFExemptDefaultRouter(DefaultRouter):
    def get_urls(self):
        urls = super().get_urls()
        return [path(url.pattern, csrf_exempt(url.callback), name=url.name) for url in urls]


router = CSRFExemptDefaultRouter()
router.register(r'users', FragabiUserViewSet)
router.register(r'assignments', QuizViewSet)
router.register(r'consultations', ConsultationViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
