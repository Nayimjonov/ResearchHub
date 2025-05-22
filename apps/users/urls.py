from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path(
        "auth/register/",
        views.UserRegisterView.as_view(),
        name="user-register",
    ),
    path(
        "auth/verify-email/",
        views.EmailVerificationView.as_view(),
        name="verify-email",
    ),
    path("auth/login/", views.UserLoginView.as_view(), name="user-login"),
    path(
        "auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"
    ),
    path("auth/logout/", views.UserLogoutView.as_view(), name="user-logout"),
    # path('auth/password-reset/', views.PasswordResetView.as_view(), name='password-reset'),
    # path('auth/password-reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path("users/me/", views.UserDataView.as_view(), name="user-me"),
    path(
        "users/<int:pk>/", views.UsersDetailView.as_view(), name="user-detail"
    ),
    path(
        "profiles/<int:id>/",
        views.UserProfileView.as_view(),
        name="user-profile",
    ),
    path("profiles/me/", views.UserProfileMeView.as_view(), name="profile-me"),
    path(
        "profiles/<int:user_id>/follow/",
        views.FollowUserView.as_view(),
        name="follow-user",
    ),
    path(
        "profiles/<int:user_id>/unfollow/",
        views.UnfollowUserView.as_view(),
        name="unfollow-user",
    ),
    path(
        "profiles/<int:user_id>/followers/",
        views.FollowersListView.as_view(),
        name="followers",
    ),
    path(
        "profiles/<int:user_id>/following/",
        views.FollowingListView.as_view(),
        name="following",
    ),
]
