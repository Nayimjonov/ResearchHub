from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import Group, GroupMember
from .serializers import GroupSerializer, GroupMemberSerializer, GroupMemberCreateSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save()

    def perform_update(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(updated_by=user)


class GroupMemberViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        group_id = self.kwargs.get("group_id")
        return GroupMember.objects.filter(group_id=group_id)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return GroupMemberCreateSerializer
        return GroupMemberSerializer

    def perform_create(self, serializer):
        group_id = self.kwargs.get("group_id")
        group = get_object_or_404(Group, id=group_id)
        user_id = self.request.data.get("user")
        user = get_object_or_404(User, id=user_id)
        serializer.save(group=group, user=user)

