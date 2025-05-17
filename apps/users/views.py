from tokenize import TokenError

from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

# from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

# from .tokens import send_password_reset_email, reset_password_confirm
# from .utils import reset_password_confirm
from .serializers import (
    UserDataSerializer,
    # PasswordResetSerializer,
    # PasswordResetConfirmSerializer
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


# # RESET PASSWORD
# class PasswordResetView(APIView):
#     def post(self, request):
#         serializer = PasswordResetSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         user = User.objects.get(email=serializer.validated_data["email"])
#         send_password_reset_email(user)
#         return Response(
#             {"detail": "Токен для сброса пароля отправлен на электронную почту."},
#             status=status.HTTP_200_OK,
#         )


# # RESET PASSWORD CONFIRM
# class PasswordResetConfirmView(APIView):
#     def post(self, request):
#         serializer = PasswordResetConfirmSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             result = reset_password_confirm(serializer.validated_data)
#             return Response(result, status=status.HTTP_200_OK)
#         except ValidationError as e:
#             return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserDataView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDataSerializer

    def get_object(self):
        return self.request.user


class UsersDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserDataSerializer
