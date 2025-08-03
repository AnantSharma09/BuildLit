from django.urls import path
from .views import ProfileDetailUpdateView

urlpatterns = [
    path("me/", ProfileDetailUpdateView.as_view(), name="profile-detail"),
]
