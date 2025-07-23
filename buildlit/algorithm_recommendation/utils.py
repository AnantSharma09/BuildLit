from buildlit.profiles.models import Profile
from buildlit.posts.models import Post
def get_recommended_post_ids(profile:Profile):
    if profile.role == 'builder':
        # for builders recommend joiners'
        return Post.objects.filter(author__role='joiner').values_list('id',flat=True)
    elif profile.role == 'joiner':
        # for joiners recommend builders
        return Post.objects.filter(author__role='builder').values_list('id', flat=True)
    return Post.objects.none() # if role is neither builder nor joiner, return no posts