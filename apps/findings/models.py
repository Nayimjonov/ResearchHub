from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class Finding(models.Model):
    VISIBILITY_CHOICES = [
        ('private', 'Private'),
        ('internal', 'Internal'),
        ('public', 'Public'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    data_summary = models.TextField()
    conclusion = models.TextField()
    significance = models.TextField()
    experiment = models.ForeignKey('experiments.Experiment', on_delete=models.CASCADE, related_name='findings')
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='findings')
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='private')
    attachments_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    citations_count = models.PositiveIntegerField(default=0)
    tags = models.CharField(max_length=200, help_text="Comma-separated tags")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='findings_created')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='findings_updated')

    def __str__(self):
        return self.title
