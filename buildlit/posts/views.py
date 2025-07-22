from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post,Media,Like,Comment, Bookmark
from .serializers import PostSerializer,MediaSerializer,BookmarkSerializer, LikeSerializer, CommentSerializer
from profiles.models import Profile
from rest_framework.permissions import IsAuthenticated

class PostListView(APIView):
    permission_classes = [IsAuthenticated]  # Make sure user is authenticated

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()  # author is handled inside serializer
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id, author=request.user.profile)
            post.delete()
            return Response({"message": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

class MediaListView(APIView):
     def get(self, request):
         media=Media.objects.all()
         serializer= MediaSerializer(media, many=True)
         return Response(serializer.data)
     def post(self, request):
            serializer= MediaSerializer(data=request.data)
            if serializer.is_valid():
                 serializer.save()
                 return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
class LikeListView(APIView):
    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        like, created = Like.objects.get_or_create(post=post, user=request.user.profile)
        if created:
            return Response({"message": "Post liked"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Post already liked"}, status=status.HTTP_200_OK)

    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            like = Like.objects.get(post=post, user=request.user.profile)
            like.delete()
            return Response({"message": "Like removed"}, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({"error": "Like not found"}, status=status.HTTP_404_NOT_FOUND)
        
class BookmarkListView(APIView):
    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        bookmark, created = Bookmark.objects.get_or_create(post=post, user=request.user.profile)
        if created:
            return Response({"message": "Post bookmarked"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Post already bookmarked"}, status=status.HTTP_200_OK)

    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            bookmark = Bookmark.objects.get(post=post, user=request.user.profile)
            bookmark.delete()
            return Response({"message": "Bookmark removed"}, status=status.HTTP_204_NO_CONTENT)
        except Bookmark.DoesNotExist:
            return Response({"error": "Bookmark not found"}, status=status.HTTP_404_NOT_FOUND)


class CommentListView(APIView):
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, user=request.user.profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
