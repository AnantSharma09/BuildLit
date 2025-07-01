from rest_framework import serializers
from . models import Post , Media , Like, Comment, Bookmark
from profiles.serializers import ProfileSerializer
from profiles.models import Profile
class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'
class PostSerializer(serializers.ModelSerializer):
    
    media = MediaSerializer(many=True, read_only=True)
    class Meta:
        model= Post
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(),write_only=True)
    post_id = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(),write_only=True)
    class Meta:
        model= Like
        fields = '__all__'
    def create(self, validated_data):
        user= validated_data.pop('user_id')
        post= validated_data.pop('post_id')
        return Like.objects.create(user=user, post=post)

class CommentSerializer(serializers.ModelSerializer):
    user= ProfileSerializer(read_only=True)
    post= PostSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), write_only=True)
    post_id = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), write_only=True)
    class Meta:
        model = Comment
        fields= '__all__'
    def create(self, validated_data):
        user = validated_data.pop('user_id')
        post = validated_data.pop('post_id')
        return Comment.objects.create(user= user, post= post, **validated_data)
class  BookmarkSerializer(serializers.ModelSerializer):
    user= ProfileSerializer(read_only=True)
    post= PostSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), write_only=True)
    post_id = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), write_only=True)

    class Meta:
        model = Bookmark
        fields= '__all__'
    def create(self, validated_data):
         user = validated_data.pop('user_id')
         post = validated_data.pop('post_id')
         return Bookmark.objects.create(user=user, post=post, **validated_data)
    
