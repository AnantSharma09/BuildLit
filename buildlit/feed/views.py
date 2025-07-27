from django.shortcuts import render
from django.http import HttpResponse
from posts.serializers import PostSerializer,LikeSerializer,CommentSerializer,BookmarkSerializer
from posts.models import Post, Like, Comment, Bookmark
from profiles.serializers import ProfileSerializer
from profiles.models import Profile
from django.contrib.auth.decorators import login_required
from algorithm_recommendation.utils import get_recommended_post_ids
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class FeedView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
       profile= Profile.objects.get(user=request.user)
       recommended_post_ids = get_recommended_post_ids(profile)
       posts=Post.objects.filter(id__in=recommended_post_ids).order_by('-created_at')
       serializer= PostSerializer(posts,many=True, context={'request': request})
       return Response(serializer.data)