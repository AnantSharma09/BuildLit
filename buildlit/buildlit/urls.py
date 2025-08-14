"""
URL configuration for buildlit project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from profiles.views import  ProfileViewSet
from feed.views import FeedView
from django.conf import settings
from django.conf.urls.static import static
from builder.views import BuilderProfileViewSet
from joiner.views import JoinerProfileViewSet, JoinerProjectViewSet, JoinerExperienceViewSet
router=DefaultRouter()


router.register(r'profile',ProfileViewSet,basename='profile')
router.register(r'builder-profile', BuilderProfileViewSet, basename='builder-profile')
router.register(r'joiner-profile', JoinerProfileViewSet, basename='joiner-profile')
router.register(r'joiner-projects', JoinerProjectViewSet, basename='joiner-projects')
router.register(r'joiner-experience', JoinerExperienceViewSet, basename='joiner-experience')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include(router.urls)),
    path('api/', include('posts.urls')),
    path('api/', include('feed.urls')),
   # path('api/', include('buildathon.urls')),
    #path('api/challenges/', include('challenges.urls')),
    path('auth/', include('authapp.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)