from django.db import models

# Create your models here.
class Profile(models.Model):
    uid = models.CharField(max_length=255, unique= True)
    Role_Choices = (
        ('builder', 'Builder'),
        ('joiner', 'Joiner'),
    )
    role = models.CharField(max_length=10, choices=Role_Choices) 
   

    # shared profile data
    bio = models.TextField(blank=True)
    skills = models.TestFileField(blank=True)
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
    

