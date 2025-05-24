from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Attachment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file_type = models.CharField(max_length=50, blank=True, null=True)
    file_url = models.URLField(max_length=500, blank=True, null=True)
    file_size = models.PositiveIntegerField(blank=True, null=True)
    content_type = models.CharField(max_length=100, blank=True, null=True)
    finding = models.ForeignKey('findings.Finding', on_delete=models.SET_NULL, null=True, blank=True, related_name='groups')
    experiment = models.ForeignKey('experiments.Experiment', on_delete=models.SET_NULL, null=True, blank=True, related_name='groups')
    project = models.ForeignKey('projects.Project', on_delete=models.SET_NULL, null=True, blank=True, related_name='groups')
    downloads_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='groups_created', null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='groups_updated', null=True, blank=True)

    def __str__(self):
        return self.title
