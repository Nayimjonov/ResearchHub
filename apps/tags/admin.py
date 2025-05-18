from django.contrib import admin
from .models import Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'category', 'usage_count', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'slug', 'category')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('-created_at',)
