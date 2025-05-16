from django.contrib.auth import get_user_model
from rest_framework import generics

from apps.users.serializers import UserRegisterSerializer

User = get_user_model()


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
