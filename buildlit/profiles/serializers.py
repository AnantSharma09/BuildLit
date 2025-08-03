# serializers.py
from rest_framework import serializers
from profiles.models import Profile, Skills, SkillWeightage
from django.contrib.auth.models import User

class SkillEntrySerializer(serializers.Serializer):
    skill = serializers.CharField(max_length=100)
    weight = serializers.IntegerField(min_value=1, max_value=5)

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    
    # Add computed field for skills from SkillWeightage
    skill_weightages = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Profile
        fields = [
            "id", "uid", "username", "email", "first_name", "last_name",
            "role", "bio", "display_name", "profile_picture", "is_onboarding_complete",
            # Joiner fields
            "experience", "education", "resume_link", "skills", "skill_weightages",
            # Builder fields
            "startup_name", "startup_description", "website", "hiring_status",
            "created_at", "updated_at"
        ]
        read_only_fields = ["id", "uid", "created_at", "updated_at", "skill_weightages"]

    def get_skill_weightages(self, obj):
        """Get skills from SkillWeightage model"""
        weightages = SkillWeightage.objects.filter(profile=obj).select_related('skill')
        return [
            {
                'skill': weightage.skill.name,
                'weight': weightage.weightage,
                'category': weightage.skill.category
            }
            for weightage in weightages
        ]

    def validate_skills(self, value):
        """Validate skills format"""
        if not isinstance(value, list):
            raise serializers.ValidationError("Skills must be a list")
        
        for skill in value:
            if not isinstance(skill, dict):
                raise serializers.ValidationError("Each skill must be an object")
            if 'skill' not in skill or 'weight' not in skill:
                raise serializers.ValidationError("Each skill must have 'skill' and 'weight' fields")
            if not isinstance(skill['weight'], int) or skill['weight'] < 1 or skill['weight'] > 5:
                raise serializers.ValidationError("Weight must be an integer between 1 and 5")
        
        return value

    def validate(self, data):
        """Cross-field validation"""
        role = data.get('role', self.instance.role if self.instance else None)
        
        if role == 'builder':
            if data.get('is_onboarding_complete') and not data.get('startup_name'):
                raise serializers.ValidationError(
                    {"startup_name": "Startup name is required for builders to complete onboarding"}
                )
        
        return data

    def create(self, validated_data):
        skills_data = validated_data.pop('skills', [])
        profile = super().create(validated_data)
        
        # Save to both JSONField and SkillWeightage models
        if skills_data:
            profile.skills = skills_data  # Save to JSONField
            profile.save()
            self._save_skill_weightages(profile, skills_data)
        
        return profile

    def update(self, instance, validated_data):
        skills_data = validated_data.pop('skills', [])
        instance = super().update(instance, validated_data)
        
        if 'skills' in self.initial_data:  # Only update skills if provided
            # Update JSONField
            instance.skills = skills_data
            instance.save()
            
            # Update SkillWeightage objects
            SkillWeightage.objects.filter(profile=instance).delete()
            if skills_data:
                self._save_skill_weightages(instance, skills_data)
        
        return instance

    def _save_skill_weightages(self, profile, skills_data):
        """Save skills to SkillWeightage model"""
        skill_weightages = []
        
        for entry in skills_data:
            skill_obj, created = Skills.objects.get_or_create(
                name=entry['skill'],
                defaults={'category': ''}  # You can add category logic here
            )
            
            skill_weightages.append(
                SkillWeightage(
                    profile=profile,
                    skill=skill_obj,
                    weightage=entry['weight']
                )
            )
        
        # Bulk create for better performance
        SkillWeightage.objects.bulk_create(skill_weightages)

class ProfileMiniSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id', 'username', 'role', 'display_name', 'profile_picture']

class SkillsSerializer(serializers.ModelSerializer):
    usage_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Skills
        fields = ['id', 'name', 'category', 'created_at', 'usage_count']
    
    def get_usage_count(self, obj):
        """Get how many profiles use this skill"""
        return SkillWeightage.objects.filter(skill=obj).count()

class SkillWeightageSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
    skill = serializers.PrimaryKeyRelatedField(queryset=Skills.objects.all())
    
    # For GET (read-only nested details)
    profile_data = ProfileMiniSerializer(source='profile', read_only=True)
    skill_data = SkillsSerializer(source='skill', read_only=True)
    
    class Meta:
        model = SkillWeightage
        fields = ['id', 'profile', 'skill', 'weightage', 'created_at', 'profile_data', 'skill_data']
        read_only_fields = ['created_at']

# Specialized serializers for different use cases
class OnboardingSerializer(serializers.ModelSerializer):
    """Simplified serializer for onboarding process"""
    
    class Meta:
        model = Profile
        fields = ['role', 'display_name', 'bio', 'skills']
    
    def update(self, instance, validated_data):
        skills_data = validated_data.pop('skills', [])
        instance = super().update(instance, validated_data)
        
        # Handle skills
        if skills_data:
            instance.skills = skills_data
            instance.save()
        
        # Mark onboarding as complete when basic info is provided
        if instance.role and instance.display_name:
            instance.is_onboarding_complete = True
            instance.save()
        
        return instance

class SkillsOnlySerializer(serializers.ModelSerializer):
    """For updating only skills"""
    
    class Meta:
        model = Profile
        fields = ['skills']
    
    def validate_skills(self, value):
        """Validate skills format"""
        if not isinstance(value, list):
            raise serializers.ValidationError("Skills must be a list")
        
        for skill in value:
            if not isinstance(skill, dict):
                raise serializers.ValidationError("Each skill must be an object")
            if 'skill' not in skill or 'weight' not in skill:
                raise serializers.ValidationError("Each skill must have 'skill' and 'weight' fields")
            if not isinstance(skill['weight'], int) or skill['weight'] < 1 or skill['weight'] > 5:
                raise serializers.ValidationError("Weight must be an integer between 1 and 5")
        
        return value
    
    def update(self, instance, validated_data):
        skills_data = validated_data.get('skills', [])
        
        # Update JSONField
        instance.skills = skills_data
        instance.save()
        
        # Update SkillWeightage objects
        SkillWeightage.objects.filter(profile=instance).delete()
        if skills_data:
            self._save_skill_weightages(instance, skills_data)
        
        return instance
    
    def _save_skill_weightages(self, profile, skills_data):
        """Save skills to SkillWeightage model"""
        skill_weightages = []
        
        for entry in skills_data:
            skill_obj, created = Skills.objects.get_or_create(
                name=entry['skill'],
                defaults={'category': ''}
            )
            
            skill_weightages.append(
                SkillWeightage(
                    profile=profile,
                    skill=skill_obj,
                    weightage=entry['weight']
                )
            )
        
        SkillWeightage.objects.bulk_create(skill_weightages)