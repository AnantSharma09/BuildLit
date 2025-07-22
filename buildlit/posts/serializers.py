from rest_framework import serializers
from . models import Post , Media , Like, Comment, Bookmark
from profiles.serializers import ProfileSerializer
from profiles.models import Profile
class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'
class PostSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    media = MediaSerializer(many=True, read_only=True)
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'post_type', 'content', 'created_at',
            'updated_at', 'media', 'like_count', 'comment_count',
            'is_liked', 'is_bookmarked'
        ]

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_is_liked(self, obj):
        user = self.context['request'].user
        return obj.likes.filter(user=user.profile).exists()

    def get_is_bookmarked(self, obj):
        user = self.context['request'].user
        return obj.bookmarks.filter(user=user.profile).exists() 
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
    
    
