from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.projects.models import Project
from apps.experiments.models import Experiment
from apps.research_groups.models import Group

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'institution', 'department', 'position', 'orcid_id',
            'is_active', 'is_staff', 'is_verified', 'date_joined',
            'role', 'citation_count', 'h_index', 'profile_url',
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


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


class ProjectSerializer(serializers.ModelSerializer):
    research_group = GroupSerializer(read_only=True)
    principal_investigator = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'short_description',
            'start_date', 'end_date', 'status', 'visibility',
            'funding_source', 'funding_amount', 'funding_currency', 'research_group',
            'principal_investigator', 'members_count','experiments_count',
            'findings_count', 'publications_count', 'tags', 'is_active', 'created_at',
            'updated_at', 'created_by', 'updated_by',
        ]


class ExperimentSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    collaborators = UserSerializer(many=True, read_only=True)
    lead_researcher = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    project_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        source='project',
        write_only=True,
        required=True
    )
    lead_researcher_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='lead_researcher',
        write_only=True,
        required=False
    )
    collaborators_id = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        source='collaborators',
        write_only=True,
        required=False
    )

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
    class Meta:
        model = Experiment
        fields = [
            'id', 'title', 'description', 'hypothesis', 'methodology', 'start_date',
            'end_date', 'status', 'project', 'project_id', 'lead_researcher', 'lead_researcher_id',
            'collaborators', 'collaborators_id', 'findings_count', 'tags', 'is_active',
            'created_at', 'updated_at', 'created_by', 'created_by_id', 'updated_by', 'updated_by_id',
        ]
