from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    institution = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    website = models.URLField(max_length=200, blank=True)
    logo = models.ImageField(upload_to='group_logos/', blank=True, null=True)
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='led_groups',
        null=True, blank=True)
    members = models.ManyToManyField(User, through='GroupMember',
        related_name='member_groups' )
    members_count = models.PositiveIntegerField(default=0)
    projects_count = models.PositiveIntegerField(default=0)
    publications_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey( User,on_delete=models.CASCADE,related_name='groups_created',
        null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='groups_updated',
        null=True, blank=True)

    def __str__(self):
        return self.name


class GroupMember(models.Model):
    ROLE_CHOICES = (
        ('member', 'Member'),
        ('leader', 'Leader'),
    )

    group = models.ForeignKey('research_groups.Group', on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('group', 'user')

    def __str__(self):
        return f"{self.user} in {self.group} as {self.role}"
