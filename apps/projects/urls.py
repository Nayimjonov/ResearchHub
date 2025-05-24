from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ProjectMemberListCreateAPIView, ProjectMemberDetailAPIView

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')


urlpatterns = [
    path('', include(router.urls)),
    path('projects/<int:project_id>/members/', ProjectMemberListCreateAPIView.as_view(), name='project-member-list-create'),
    path('projects/<int:project_id>/members/<int:member_id>/', ProjectMemberDetailAPIView.as_view(), name='project-member-update'),
]

