from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from profiles.models import Profile  # import your profile model

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        role = request.data.get("role")

        if not all([username, email, password, role]):
            return Response(
                {"error": "All fields (username, email, password, role) are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create user (this will trigger the signal to auto-create Profile)
        user = User.objects.create_user(username=username, email=email, password=password)

        # ✅ Update the profile with role (OneToOneField allows this directly)
        profile = user.profile
        profile.role = role
        profile.save()

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "username": user.username,
                    "email": user.email,
                    "role": profile.role,
                },
            },
            status=status.HTTP_201_CREATED,
        )
