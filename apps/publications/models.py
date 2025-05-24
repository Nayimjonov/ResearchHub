from django.db import models
from django.conf import settings

class Publication(models.Model):
    title = models.CharField(max_length=200)
    abstract = models.TextField()
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='publications')
    journal = models.CharField(max_length=100, blank=True, null=True)
    conference = models.CharField(max_length=100, blank=True, null=True)
    publication_date = models.DateField()
    doi = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(max_length=300, blank=True, null=True)
    citation = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50)
    project = models.ForeignKey('projects.Project', on_delete=models.SET_NULL, null=True, related_name='publications')
    findings = models.ForeignKey('findings.Finding', on_delete=models.SET_NULL, null=True, related_name='publications')  # Agar mavjud bo‘lsa
    citations_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    downloads_count = models.PositiveIntegerField(default=0)
    tags = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='created_publications')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='updated_publications')

    def __str__(self):
        return self.title
