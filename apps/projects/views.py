from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import Project, ProjectMember
from .serializers import ProjectSerializer, ProjectMemberSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save()

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class ProjectMemberListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProjectMemberSerializer
    permission_classes = [AllowAny]
    lookup_url_kwarg = 'project_id'

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return ProjectMember.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_id')
        project = get_object_or_404(Project, id=project_id)
        serializer.save(project=project)


class ProjectMemberDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMemberSerializer
    permission_classes = [AllowAny]
    lookup_url_kwarg = 'member_id'

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return ProjectMember.objects.filter(project_id=project_id)

