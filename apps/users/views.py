from tokenize import TokenError

from common.pagination import (
    ProfileFollowersPagination,
    ProfileFollowingPagination,
)
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import UserProfile
from .serializers import (
    UserDataSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserRegisterSerializer,
)

User = get_user_model()


# USER-REGISTER
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


# VERIFY-EMAIL


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


class UserProfileView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    lookup_field = "id"


class UserProfileMeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)


class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        if request.user.id == user_id:
            return Response(
                {"detail": "Нельзя подписаться на самого себя."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_to_follow = get_object_or_404(User, pk=user_id)
        profile = request.user.profile

        if user_to_follow.profile in profile.following.all():
            return Response(
                {"detail": "Уже подписаны."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        profile.following.add(user_to_follow.profile)
        return Response(
            {"detail": "Подписка выполнена."}, status=status.HTTP_200_OK
        )


class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        if request.user.id == user_id:
            return Response(
                {"detail": "Нельзя отписаться от самого себя."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_to_unfollow = get_object_or_404(User, pk=user_id)
        profile = request.user.profile

        if user_to_unfollow.profile not in profile.following.all():
            return Response(
                {"detail": "Вы не подписаны."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        profile.following.remove(user_to_unfollow.profile)
        return Response(
            {"detail": "Отписка выполнена."}, status=status.HTTP_200_OK
        )


class FollowersListView(generics.ListAPIView):
    serializer_class = UserDataSerializer
    pagination_class = ProfileFollowersPagination

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs["user_id"])
        return User.objects.filter(profile__following=user.profile)


class FollowingListView(generics.ListAPIView):
    serializer_class = UserDataSerializer
    pagination_class = ProfileFollowingPagination

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs["user_id"])
        followed_profiles = user.profile.following.all()
        return User.objects.filter(profile__in=followed_profiles)
