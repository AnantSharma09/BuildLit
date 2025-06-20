from rest_framework import serializers
from profiles.models import Profile, Skills, SkillWeightage

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields = '__all__'
        read_only_fields = ['created_at']


