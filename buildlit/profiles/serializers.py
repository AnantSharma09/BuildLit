from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "user", "role", "profile_picture", "display_name"]
        read_only_fields = ["user"]

    def update(self, instance, validated_data):
        new_role = validated_data.get("role", instance.role)
        # enforce role only once
        if instance.role and new_role and new_role != instance.role:
            raise serializers.ValidationError("Role is already set and cannot be changed in MVP.")
        return super().update(instance, validated_data)

