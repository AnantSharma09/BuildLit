# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


class Profile(models.Model):
    class Role(models.TextChoices):
        JOINER = 'joiner', _('Joiner')
        BUILDER = 'builder', _('Builder')

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    # === Common Fields ===
    role = models.CharField(max_length=10, choices=Role.choices, blank=True)  # Allow blank for initial creation
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to="avatars/", null=True, blank=True)
    display_name = models.CharField(max_length=100, blank=True)
    is_onboarding_complete = models.BooleanField(default=False)

    # === Joiner Fields ===
    experience = models.PositiveIntegerField(null=True, blank=True, help_text="Years of experience")
    education = models.CharField(max_length=255, blank=True)
    resume_link = models.URLField(blank=True)

    # Skill & Tech stack as weighted skills
    skills = models.JSONField(default=list, blank=True)

    # === Builder Fields ===
    startup_name = models.CharField(max_length=255, blank=True)
    startup_description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    hiring_status = models.BooleanField(default=False)

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    

# Auto-create profile when user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

# Keep these models if you want the normalized approach as well
# Otherwise, you can remove them if you're only using JSONField
class Skills(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['category', 'name']
        verbose_name_plural = "Skills"
    
    def __str__(self):
        return self.name

class SkillWeightage(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skill_weightages')
    skill = models.ForeignKey(Skills, on_delete=models.CASCADE)
    weightage = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['profile', 'skill']
        ordering = ['-weightage']
    
    def __str__(self):
        return f"{self.profile.user.username} - {self.skill.name} ({self.weightage})"
