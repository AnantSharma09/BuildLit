from django.db import models

# Create your models here.


class StartupProfile(models.Model):
    founder = models.CharField(max_length=250, unique=True)
    co-founder= models.CharField(max_length=250, blank=True)
    startup_name = models.CharField(max_length=255, blank=True)
    startup_description = models.TextField(blank=True)
    is_deployed = models.BooleanField(default=False)
    website_url = models.URLField(blank=True)
    industry = models.CharField(max_length=100, blank=True)
    is_funded= models.BooleanField(default=False)
    looking_for_inversotrs = models.BooleanField(default=False)
    current_teamSize = models.IntegerField(default=1)
    number_of_users = models.IntegerField(default=0)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.founder} - {self.startup_name} ({self.industry})"
    
