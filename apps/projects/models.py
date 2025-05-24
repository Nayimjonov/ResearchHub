from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    short_description = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50)
    visibility = models.CharField(max_length=50)
    funding_source = models.CharField(max_length=100)
    funding_amount = models.DecimalField(max_digits=12, decimal_places=2)
    funding_currency = models.CharField(max_length=10)
    research_group = models.ForeignKey('research_groups.Group', on_delete=models.SET_NULL, null=True)
    principal_investigator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    members_count = models.IntegerField(default=0)
    experiments_count = models.IntegerField(default=0)
    findings_count = models.IntegerField(default=0)
    publications_count = models.IntegerField(default=0)
    tags = models.CharField(max_length=255, default="")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='created_projects')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='updated_projects')

    def __str__(self):
        return self.title

class ProjectMember(models.Model):
    ROLE_CHOICES = (
        ('member', 'Member'),
        ('leader', 'Leader'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('project', 'user')

    def __str__(self):
        return f"{self.user} in {self.project} as {self.role}"