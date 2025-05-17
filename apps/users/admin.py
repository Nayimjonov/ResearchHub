from django.contrib import admin

from .models import User, UserProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "role")
    list_filter = ("role", "is_verified")
    search_fields = ("email", "first_name", "last_name")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "projects_count", "publications_count")
    search_fields = ("user__email", "bio", "research_interests")
