from django.contrib.auth import get_user_model
from rest_framework import generics
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
