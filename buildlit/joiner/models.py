from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import URLValidator

User = get_user_model()

class JoinerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="joiner_profile")
    bio = models.TextField(blank=True, null=True)
    skills = models.JSONField(blank=True, null=True, help_text="List of skills as JSON")
    link = models.URLField(
        blank=True, null=True,
        validators=[URLValidator()],
        help_text='Enter your GitHub profile link.'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Joiner Profile"


class JoinerProject(models.Model):
    profile = models.ForeignKey(JoinerProfile, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    tech_stack = models.JSONField(blank=True, null=True, help_text="List of technologies used")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class JoinerExperience(models.Model):
    profile = models.ForeignKey(JoinerProfile, on_delete=models.CASCADE, related_name="experiences")
    company = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.role} at {self.company}"

