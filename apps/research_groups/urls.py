from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroupViewSet, GroupMemberViewSet

router = DefaultRouter()
router.register(r'research-groups', GroupViewSet, basename='research-group')
router.register(r'research-groups/(?P<group_id>\d+)/members', GroupMemberViewSet, basename='group-members')


urlpatterns = [
    path('', include(router.urls)),
]
