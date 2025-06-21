from rest_framework import serializers
from profiles.models import Profile, Skills, SkillWeightage

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields = '__all__'
        read_only_fields = ['created_at']


class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model= Skills
        fields = '__all__'

class SkillWeightageSerializer(serializers.ModelSerializer):
    # for post/put requests, we need to use PrimaryKeyRelatedField
    profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
    skill =  serializers.PrimaryKeyRelatedField(queryset=Skills.objects.all())
    # for get requests, we can use the SkillsSerializer to get full skill details
    profile_data = ProfileSerializer(source='profile', read_only=True)
    skill_data = SkillsSerializer(source='skill', read_only=True)


  
    class Meta:
        model=SkillWeightage
        fields= ['id','profile','weightage','created_at','profile_data','skill_data']
        read_only_fields = ['created_at']