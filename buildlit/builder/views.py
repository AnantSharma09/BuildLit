from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import BuilderProfileSerializer
from .models import BuilderProfile
from core.permissions import IsBuilder
from rest_framework.exceptions import PermissionDenied
# Create your views here.
class BuilderProfileViewSet(ModelViewSet):
    queryset = BuilderProfile.objects.all()
    serializer_class = BuilderProfileSerializer
    permission_classes = [IsAuthenticated,IsBuilder]
    
    def get_queryset(self):
      return BuilderProfile.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        if BuilderProfile.objects.filter(user=self.request.user).exists():
            raise PermissionDenied("Builder profile already exists.")
        if self.request.user.profile.role != "builder":
         raise PermissionDenied("Only builders can create a BuilderProfile.")
        serializer.save(user=self.request.user)

