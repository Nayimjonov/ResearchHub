from tokenize import TokenError

from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (  # VerifyEmailSerializer
    UserLoginSerializer,
    UserRegisterSerializer,
)

User = get_user_model()


# USER-REGISTER
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


# VERIFY-EMAIL
# class EmailVerificationView(APIView):
#     def post(self, request):
#         serializer = VerifyEmailSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"detail": "Email успешно подтвержден."}, status=200)


# USER-LOGIN
class UserLoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer


# USER-LOGOUT
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Необходим refresh токен."}, status=400)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response({"detail": "Недопустимый токен."}, status=401)
        return Response({"detail": "Вы успешно вышли из системы."}, status=204)
