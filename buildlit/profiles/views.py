from django.shortcuts import render
from rest_framework import viewsets
from profiles.models import Profile,Skills,SkillWeightage
from profiles.serializers import ProfileSerializer, SkillsSerializer, SkillWeightageSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class SkillsViewSet(viewsets.ModelViewSet):
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializer

class SkillWeightageViewSet(viewsets.ModelViewSet):
    queryset = SkillWeightage.objects.all()
    serializer_class = SkillWeightageSerializer


