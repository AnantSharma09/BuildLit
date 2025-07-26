from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    Role_Choices = (
        ('builder', 'Builder'),
        ('joiner', 'Joiner'),
    )
    role = models.CharField(max_length=10, choices=Role_Choices) 
   

    # shared profile data
    bio = models.TextField(blank=True)
    Age = models.IntegerField(null=True, blank=True)

    # Joiner-specific profile data
    experience = models.IntegerField(null=True, blank=True)
    education = models.TextField(blank=True)
    Projects = models.TextField(blank=True)
    Links = models.TextField(blank=True)
    Resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    # Builder-specific profile data
    Startup_name = models.CharField(max_length=255, blank=True)
    Startup_description = models.TextField(blank=True)
    is_Deployed = models.BooleanField(default=False)
    startup_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.uid} - {self.role}"



# skill model to store skills (i need to hardcode the skills for now)
class Skills(models.Model):
    name=models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

#skill weightage model to store the weightage of each skills for each profile
class SkillWeightage(models.Model):
    profile= models.ForeignKey(Profile, on_delete=models.CASCADE )
    skill = models.ForeignKey(Skills, on_delete=models.CASCADE)
    weightage= models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return f"{self.profile.uid} - {self.skill.name} ({self.weightage})"
        
    

