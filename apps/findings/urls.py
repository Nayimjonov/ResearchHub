from rest_framework.routers import DefaultRouter
from apps.findings.views import FindingViewSet

router = DefaultRouter()
router.register(r'findings', FindingViewSet, basename='finding')

urlpatterns = router.urls
