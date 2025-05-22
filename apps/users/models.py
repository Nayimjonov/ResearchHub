from django.contrib.auth.models import AbstractUser
from django.db import models

from .manager import UserManager


class User(AbstractUser):
    ROLE_CHOICES = [
        ("user", "User"),
        ("admin", "Admin"),
    ]

    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    institution = models.CharField(max_length=200, blank=True, null=True)
    department = models.CharField(max_length=200, blank=True, null=True)
    position = models.CharField(max_length=200)
    orcid_id = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    role = models.CharField(
        max_length=50, choices=ROLE_CHOICES, default="user"
    )
    citation_count = models.PositiveIntegerField(default=0)
    h_index = models.PositiveIntegerField(default=0)
    profile_url = models.URLField(blank=True)
    email_token = models.CharField(max_length=64, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    bio = models.TextField(max_length=300, blank=True, null=True)
    research_interests = models.TextField(
        max_length=300, blank=True, null=True
    )
    avatar = models.ImageField(
        upload_to="user-profile-images/", blank=True, null=True
    )
    website = models.URLField(blank=True, null=True)
    google_scholar = models.URLField(blank=True, null=True)
    researchgate = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    followers = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="following",
        blank=True,
    )
    projects_count = models.PositiveIntegerField(default=0)
    publications_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
