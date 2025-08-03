# views.py
from django.shortcuts import render
from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from profiles.models import Profile, Skills, SkillWeightage
from profiles.serializers import (
    ProfileSerializer, SkillsSerializer, SkillWeightageSerializer,
    OnboardingSerializer, SkillsOnlySerializer, ProfileMiniSerializer
)
from rest_framework.permissions import IsAuthenticated
class ProfileDetailUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    def get_serializer_class(self):
        """Use different serializers based on the action"""
        if self.request.method == 'PATCH':
            # Check if only updating skills
            if set(self.request.data.keys()) == {'skills'}:
                return SkillsOnlySerializer
        return ProfileSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all().select_related('user')
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter based on user permissions"""
        if self.action == 'list':
            # Only show profiles that have completed onboarding
            return Profile.objects.filter(is_onboarding_complete=True).select_related('user')
        return super().get_queryset()
    
    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        """Get or update current user's profile"""
        profile = request.user.profile
        
        if request.method == 'GET':
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        
        elif request.method == 'PATCH':
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['patch'])
    def onboard(self, request):
        """Handle onboarding process"""
        profile = request.user.profile
        serializer = OnboardingSerializer(profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Onboarding updated successfully',
                'is_complete': profile.is_onboarding_complete
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['patch'])
    def update_skills(self, request):
        """Update only skills"""
        profile = request.user.profile
        serializer = SkillsOnlySerializer(profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Skills updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def skills(self, request, pk=None):
        """Get skills for a specific profile"""
        profile = self.get_object()
        skill_weightages = SkillWeightage.objects.filter(profile=profile).select_related('skill')
        serializer = SkillWeightageSerializer(skill_weightages, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def builders(self, request):
        """Get all builder profiles"""
        builders = Profile.objects.filter(
            role='builder', 
            is_onboarding_complete=True
        ).select_related('user')
        serializer = ProfileMiniSerializer(builders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def joiners(self, request):
        """Get all joiner profiles"""
        joiners = Profile.objects.filter(
            role='joiner', 
            is_onboarding_complete=True
        ).select_related('user')
        serializer = ProfileMiniSerializer(joiners, many=True)
        return Response(serializer.data)

class SkillsViewSet(viewsets.ModelViewSet):
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get most popular skills"""
        from django.db.models import Count
        
        popular_skills = Skills.objects.annotate(
            usage_count=Count('skillweightage')
        ).filter(usage_count__gt=0).order_by('-usage_count')[:20]
        
        serializer = SkillsSerializer(popular_skills, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get skill categories"""
        categories = Skills.objects.values_list('category', flat=True).distinct()
        return Response({'categories': [cat for cat in categories if cat]})

class SkillWeightageViewSet(viewsets.ModelViewSet):
    queryset = SkillWeightage.objects.all().select_related('profile__user', 'skill')
    serializer_class = SkillWeightageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter by profile if specified"""
        queryset = super().get_queryset()
        profile_id = self.request.query_params.get('profile', None)
        
        if profile_id:
            queryset = queryset.filter(profile_id=profile_id)
        
        return queryset
