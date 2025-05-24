from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class Experiment(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    hypothesis = models.TextField()
    methodology = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='experiments')
    lead_researcher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='led_experiments')
    collaborators = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='experiment_collaborations', blank=True)
    findings_count = models.PositiveIntegerField(default=0)
    tags = models.CharField(max_length=200, help_text="Comma-separated tags")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='experiments_created')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='experiments_updated')

    def __str__(self):
        return self.title
