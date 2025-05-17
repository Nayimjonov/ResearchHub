from django.contrib.auth import get_user_model
from rest_framework import generics

from .serializers import UserRegisterSerializer  # VerifyEmailSerializer

User = get_user_model()


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


# class EmailVerificationView(APIView):
#     def post(self, request):
#         serializer = VerifyEmailSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"detail": "Email успешно подтвержден."}, status=200)
