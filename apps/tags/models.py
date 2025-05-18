from django.db import models
from django.utils.text import slugify

class Tag(models.Model):
    CATEGORY_CHOICES = [
        ('discipline', 'Discipline'),
        ('technology', 'Technology'),
        ('method', 'Method'),
    ]
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    usage_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
