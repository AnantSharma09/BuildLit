from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Profile
from .serializers import ProfileSerializer
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

user = get_user_model()
class ProfileViewSet(ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # prevent duplicate manual creations; rely on signal
        if Profile.objects.filter(user=self.request.user).exists():
            raise ValidationError("Profile already exists.")
        serializer.save(user=self.request.user)
