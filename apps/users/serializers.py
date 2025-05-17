from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


# REGISTER
class UserRegisterSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    full_name = serializers.CharField(read_only=True)
    institution = serializers.CharField()
    department = serializers.CharField()
    position = serializers.CharField()
    orcid_id = serializers.CharField()
    is_active = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    role = serializers.CharField(read_only=True)
    citation_count = serializers.IntegerField(read_only=True)
    h_index = serializers.IntegerField(read_only=True)
    profile_url = serializers.URLField(read_only=True)

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError(
                {"password": "Пароли не совпадают."}
            )
        return data

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("password_confirm")

        user = User.objects.create_user(password=password, **validated_data)
        return user


# VERIFY_EMAIL
# class VerifyEmailSerializer(serializers.Serializer):
#     token = serializers.CharField(required=True)
#
#     def validate(self, attrs):
#         token = attrs.get("token")
#         try:
#             user = User.objects.get(email_token=token)
#         except User.DoesNotExist:
#             raise serializers.ValidationError(
#                 {"token": "Недействительный или просроченный токен."}
#             )
#
#         attrs["user"] = user
#         return attrs
#
#     def save(self, **kwargs):
#         user = self.validated_data["user"]
#         user.is_verified = True
#         user.is_active = True
#         user.email_token = None
#         user.save()
#         return user


# LOGIN DATA
class UserLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        user_data = UserRegisterSerializer(self.user).data

        response_data = {
            "access": data["access"],
            "refresh": data["refresh"],
            "user": user_data,
        }
        return response_data
