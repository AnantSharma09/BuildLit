from rest_framework import serializers
from .models import JoinerProfile, JoinerProject, JoinerExperience

class JoinerProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinerProject
        fields = ["id", "title", "description", "link", "tech_stack"]
        extra_kwargs = {"id": {"read_only": True}}


class JoinerExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinerExperience
        fields = ["id", "company", "role", "start_date", "end_date", "description"]
        extra_kwargs = {"id": {"read_only": True}}


class JoinerProfileSerializer(serializers.ModelSerializer):
    projects = JoinerProjectSerializer(many=True, required=False)
    experiences = JoinerExperienceSerializer(many=True, required=False)

    class Meta:
        model = JoinerProfile
        fields = ["id", "user", "bio", "skills", "link", "projects", "experiences"]
        extra_kwargs = {
            "user": {"read_only": True}
        }

    def create(self, validated_data):
        projects_data = validated_data.pop("projects", [])
        experiences_data = validated_data.pop("experiences", [])

        # Attach profile to current user
        user = self.context["request"].user
        profile = JoinerProfile.objects.create(user=user, **validated_data)

        for project_data in projects_data:
            JoinerProject.objects.create(profile=profile, **project_data)

        for experience_data in experiences_data:
            JoinerExperience.objects.create(profile=profile, **experience_data)

        return profile

    def update(self, instance, validated_data):
        projects_data = validated_data.pop("projects", None)
        experiences_data = validated_data.pop("experiences", None)

        instance.bio = validated_data.get("bio", instance.bio)
        instance.skills = validated_data.get("skills", instance.skills)
        instance.link = validated_data.get("link", instance.link)
        instance.save()

        if projects_data is not None:
            instance.projects.all().delete()
            for project_data in projects_data:
                JoinerProject.objects.create(profile=instance, **project_data)

        if experiences_data is not None:
            instance.experiences.all().delete()
            for experience_data in experiences_data:
                JoinerExperience.objects.create(profile=instance, **experience_data)

        return instance
