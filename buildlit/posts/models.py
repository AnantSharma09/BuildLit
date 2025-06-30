from django.db import models
from django.utils import timezone
from profiles.models import Profile
import uuid

# ------------------------
# Post Model
# ------------------------

class Post(models.Model):
    POST_TYPES = [
        ('update', 'Update'),
        ('question', 'Question'),
        ('idea', 'Idea'),
        ('resource', 'Resource'),
        ('project', 'Project'),
        ('opportunity', 'Opportunity'),
        ('other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=2000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author.user.username} - {self.content[:40]}"


# ------------------------
# Media Upload Function
# ------------------------

def upload_to(instance, filename):
    username = instance.post.author.user.username
    post_id = instance.post.id or 'temp'
    return f'post_media/{username}/{post_id}/{filename}'


# ------------------------
# Media Model
# ------------------------

class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media')
    file = models.FileField(upload_to=upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Media for Post {self.post.id}'


# ------------------------
# Like Model
# ------------------------

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='likes')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.user.username} liked {self.post.id}"


# ------------------------
# Comment Model
# ------------------------

class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user.username} commented on {self.post.id}"


# ------------------------
# Bookmark Model
# ------------------------

class Bookmark(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='bookmarks')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='bookmarks')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.user.username} bookmarked {self.post.id}"
