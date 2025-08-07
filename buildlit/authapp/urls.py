# auth/urls.py
from django.urls import path
from .views import SignupView
from .views import EmailTokenObtainPairView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', EmailTokenObtainPairView.as_view(), name="login"),  # Handles login
]
