# auth/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import EmailTokenObtainPairSerializer
from django.db import transaction
from django.utils.text import slugify
 
User = get_user_model()
# authapp/views.py
# authapp/views.py
from django.db import transaction
from django.utils.text import slugify

class SignupView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        username = (request.data.get("username") or "").strip()
        password = (request.data.get("password") or "").strip()
        email = (request.data.get("email") or "").strip().lower()

        if not username or not password or not email:
            return Response({"error": "All fields required"}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=400)

        if User.objects.filter(username=username).exists():
            # fallback: make username unique
            base = slugify(username) or "user"
            i = 1
            new_username = base
            while User.objects.filter(username=new_username).exists():
                i += 1
                new_username = f"{base}{i}"
            username = new_username

        user = User.objects.create_user(username=username, password=password, email=email)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "message": "Signup successful"
        }, status=status.HTTP_201_CREATED)


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer
