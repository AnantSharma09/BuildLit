from django.shortcuts import render
from rest_framework import  status , viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Buildathon,BuildathonQuestion,BuildathonWinner,BuildathonSubmission,BuildathonJudging
from .serializers import BuildathonSerializer, BuildathonQuestionSerializer,QuestionAttachmentSerializer,BuildathonWinnerSerializer,BuildathonSubmissionSerializer,BuildathonJudgingSerializer
from profiles.serializers import ProfileMiniSerializer
from profiles.models import Profile
from rest_framework.permissions import BasePermission,SAFE_METHODS
from django.core.exceptions import PermissionDenied
from rest_framework.decorators import action  
from django_filters.rest_framework import DjangoFilterBackend 
from django.shortcuts import get_object_or_404
# Create your views here.

class IsAdminOrReadOnly(BasePermission):
    """
     Allows read-only access to all authenticated users.
     Only admin users can write (create/update/delete).
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class BuildathonViewSet(viewsets.ModelViewSet):
    queryset = Buildathon.objects.all()
    serializer_class =BuildathonSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def register(self, request,pk=None):
        buildathon = self.get_object()
        user = request.user

        if buildathon.registered_participants.filter(id=user.id).exists():
            return Response({
                "message": "You are already registered for this buildathon."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        buildathon.registered_participants.add(user)
        return Response({
            "message": "You have successfully registered for the buildathon."
        }, status=status.HTTP_200_OK)



class BuildathonQuestionViewSet(viewsets.ModelViewSet):
    queryset = BuildathonQuestion.objects.all()
    serializer_class = BuildathonQuestionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
   

class BuildathonWinnerView(viewsets.ModelViewSet):
    queryset = BuildathonWinner.objects.all()
    serializer_class = BuildathonWinnerSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'],permission_classes=[IsAdminOrReadOnly])
    def declare(self,request):
        buildathon_id = request.data.get('buildathon_id')
        top_n = request.data.get('top_n',3)

        if not buildathon_id:
            return Response({"error": "Buildathon ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        buildathon = get_object_or_404(Buildathon, id=buildathon_id)
        
        top_submissions = BuildathonSubmission.objects.filter(buildathon=buildathon).order_by('-score')[:top_n]

        if not top_submissions:
            return Response({"message": "No submissions found for this buildathon."}, status=404)
        
        winners=[]
        BuildathonWinner.objects.filter(buildathon=buildathon).delete()
        for rank , response in enumerate(top_submissions, start=1):
            winner = BuildathonWinner.objects.create(
                buildathon=buildathon,
                user = response.participant.user,
                rank = rank
            )
            winners.append(winner)

        serialize = self.get_serializer(winners, many=True)
        return Response(serialize.data, status=status.HTTP_201_CREATED)
      
    @action(detail=False,methods=['get'], url_path='by_buildathon/(?P<buildathon_id>[^/.]+)')
    def winners(self, request,buildathon_id=None):
        buildathon = get_object_or_404(Buildathon, id=buildathon_id)
        
        winners = BuildathonWinner.objects.filter(buildathon=buildathon).order_by('rank')
        if not winners:
            return Response({"message": "No winner yet."}, status=status.HTTP_204_NO_CONTENT)
        
        serializer = self.get_serializer(winners, many=True)
        return Response(serializer.data, status=200)
    

class BuildathonSubmissionViewSet(viewsets.ModelViewSet):
    queryset = BuildathonSubmission.objects.all()
    serializer_class = BuildathonSubmissionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['buildathon', 'question']

    def perform_create(self, serializer):
        try:
            profile = Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            raise PermissionDenied("You must have a profile to submit to a buildathon.")
        
        serializer.save(participant=profile)

    def get_queryset(self):
        user  = self.request.user
        if user.is_staff:
            return BuildathonSubmission.objects.all()
        try:
            profile = Profile.objects.get(user=user)
            return BuildathonSubmission.objects.filter(participant=profile)
        except Profile.DoesNotExist:
            return BuildathonSubmission.objects.none()
        

class BuildathonJudgingViewSet(viewsets.ModelViewSet):
    serializer_class = BuildathonJudgingSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = BuildathonJudging.objects.all()
    def get_queryset(self):
        try:
            profile = Profile.objects.get(user=self.request.user)
            return BuildathonJudging.objects.filter(judge=profile)
        except Profile.DoesNotExist:
            return BuildathonJudging.objects.none()
        
    def perform_create(self, serializer):
       profile = get_object_or_404(Profile, user=self.request.user)
