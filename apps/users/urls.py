from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path(
        "auth/register/",
        views.UserRegisterView.as_view(),
        name="user-register",
    ),
    # path(
    #     "auth/verify-email/",
    #     views.EmailVerificationView.as_view(),
    #     name="verify-email",
    # ),
    path("auth/login/", views.UserLoginView.as_view(), name="user-login"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("auth/logout/", views.UserLogoutView.as_view(), name="user-logout"),
    # path('auth/password-reset/', views.PasswordResetView.as_view(), name='password-reset'),
    # path('auth/password-reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('users/me/', views.UserDataView.as_view(), name='user-me'),

]
