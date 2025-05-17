from django.urls import path

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
]
