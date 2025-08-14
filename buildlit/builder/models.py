from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
class BuilderProfile(models.Model):
    # Basic startup description level questions
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    startup_name = models.CharField(max_length=100)
    startup_idea = models.TextField()

    STAGE_CHOICES = [
        ("ideation", "Ideation"),
        ("pre-launch", "Pre-Launch"),
        ("launched", "Launched"),
    ]
    startup_stage = models.CharField(max_length=20, choices=STAGE_CHOICES)

    STARTUP_CATEGORY_CHOICES = [
        ('AI', 'AI/ML'),
        ('FINTECH', 'Fintech'),
        ('EDTECH', 'EdTech'),
        ('HEALTHTECH', 'HealthTech'),
        ('SAAS', 'SaaS'),
        ('WEB3', 'Web3'),
        ('MARKETPLACE', 'Marketplace'),
        ('SOCIAL', 'Social Media'),
        ('GAMING', 'Gaming'),
        ('E_COMMERCE', 'E-commerce'),
        ('OTHER', 'Other'),
    ]
    startup_category = models.CharField(
        max_length=30,
        choices=STARTUP_CATEGORY_CHOICES,
        default='OTHER',
        help_text='Choose the category that best describes your startup.'
    )

    IS_DEPLOYED = models.BooleanField()

    # ✅ NEW: Dropdown field for "What describes your startup well?"
    STARTUP_DESCRIPTION_CHOICES = [
        ('INNOVATIVE', 'Innovative'),
        ('SCALABLE', 'Scalable'),
        ('BOOTSTRAPPED', 'Bootstrapped'),
        ('VC_FUNDED', 'VC Funded'),
        ('TEAM_BASED', 'Team Based'),
        ('SOLO_FOUNDER', 'Solo Founder'),
        ('COMMUNITY_DRIVEN', 'Community Driven'),
        ('EXPERIMENTAL', 'Experimental'),
        ('IMPACT_FOCUSED', 'Impact Focused'),
        ('STEALTH', 'Stealth Mode'),
    ]
    startup_description = models.CharField(
        max_length=30,
        choices=STARTUP_DESCRIPTION_CHOICES,
        default='INNOVATIVE',
        help_text='Choose the phrase that best describes your startup.'
    )

    def __str__(self):
        return self.startup_name

