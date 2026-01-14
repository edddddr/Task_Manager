from rest_framework.permissions import IsAuthenticated
from rest_framework import status, permissions
from rest_framework.views import APIView
from .models import User
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.throttles import LogoutThrottle, RegisterThrottle, LoginThrottle
from rest_framework_simplejwt.views import TokenObtainPairView




class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [RegisterThrottle]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )



class LoginView(TokenObtainPairView):
    throttle_classes = [LoginThrottle]



class LogoutView(APIView):
    throttle_classes = [LogoutThrottle]
    permission_classes = [IsAuthenticated]


    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"detail": "Successfully logged out"},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception:
            return Response(
                {"detail": "Invalid refresh token"},
                status=status.HTTP_400_BAD_REQUEST,
            )
