from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Group, GroupMember

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'institution', 'department', 'position', 'orcid_id',
            'is_active', 'is_staff', 'is_verified', 'date_joined',
            'role', 'citation_count', 'h_index', 'profile_url'
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class GroupSerializer(serializers.ModelSerializer):
    leader = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    created_by_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='created_by',
        write_only=True,
        required=False
    )
    updated_by_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='updated_by',
        write_only=True,
        required=False
    )
    leader_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='leader',
        write_only=True,
        required=False
    )

    class Meta:
        model = Group
        fields = [
            'id', 'name', 'description', 'institution', 'department', 'website', 'logo',
            'leader', 'leader_id',
            'members_count', 'projects_count', 'publications_count',
            'is_active', 'created_at', 'updated_at',
            'created_by', 'created_by_id', 'updated_by', 'updated_by_id'
        ]

class GroupMemberSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = GroupMember
        fields = ["id", "group", "user", "role", "joined_at", "is_active", "created_at", "updated_at"]


class GroupMemberCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = GroupMember
        fields = ["user", "role"]

