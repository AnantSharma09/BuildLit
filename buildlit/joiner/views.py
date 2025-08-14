from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import JoinerProfile, JoinerProject, JoinerExperience
from .serializers import (
    JoinerProfileSerializer,
    JoinerProjectSerializer,
    JoinerExperienceSerializer
)
from core.permissions import IsJoiner

class JoinerProfileViewSet(ModelViewSet):
    serializer_class = JoinerProfileSerializer
    permission_classes = [IsAuthenticated,IsJoiner]

    def get_queryset(self):
        return JoinerProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        
     if self.request.user.profile.role != "joiner":
        raise PermissionDenied("Only joiners can create a JoinerProfile.")
     if JoinerProfile.objects.filter(user=self.request.user).exists():
            raise PermissionDenied("Joiner profile already exists.")

     serializer.save(user=self.request.user)


class JoinerProjectViewSet(ModelViewSet):
    serializer_class = JoinerProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JoinerProject.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
     if self.request.user.profile.role != "joiner":
        raise PermissionDenied("Only joiners can create a JoinerProfile.")
     try:
       profile = JoinerProfile.objects.get(user=self.request.user)
     except JoinerProfile.DoesNotExist:
      raise PermissionDenied("You must create a joiner profile first.")

     serializer.save(profile=profile)


class JoinerExperienceViewSet(ModelViewSet):
    serializer_class = JoinerExperienceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JoinerExperience.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
     if self.request.user.profile.role != "joiner":
        raise PermissionDenied("Only joiners can create a JoinerProfile.")
     profile = JoinerProfile.objects.get(user=self.request.user)
     serializer.save(profile=profile)
