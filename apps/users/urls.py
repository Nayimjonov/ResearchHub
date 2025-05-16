from django.urls import path

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
]
