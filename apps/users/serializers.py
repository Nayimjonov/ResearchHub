from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.cache import cache
from rest_framework import serializers
from .tokens import send_verification_token
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



# LOGIN DATA
class UserLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        user_data = UserDataSerializer(self.user).data

        response_data = {
            "access": data["access"],
            "refresh": data["refresh"],
            "user": user_data,
        }
        return response_data


# # PASSWORD-RESET
# class PasswordResetSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#
#     def validate_email(self, value):
#         if not User.objects.filter(email=value).exists():
#             raise serializers.ValidationError("Пользователь с таким email не найден.")
#         return value
#
#
# # PASSWORD-RESET-CONFIRM
# class PasswordResetConfirmSerializer(serializers.Serializer):
#     token = serializers.CharField()
#     password = serializers.CharField(min_length=8)
#     password_confirm = serializers.CharField(min_length=8)
#
#     def validate(self, attrs):
#         self._validate_password(attrs)
#         self._validate_token(attrs['token'])
#         return attrs
#
#     def _validate_password(self, attrs):
#         password, password_confirm = attrs['password'], attrs['password_confirm']
#
#         if password != password_confirm:
#             raise serializers.ValidationError("Пароль и подтверждение пароля не совпадают.")
#
#         if len(password) < 8 or not any(char.isalpha() for char in password):
#             raise serializers.ValidationError("Пароль должен быть не менее 8 символов и содержать хотя бы одну букву.")
#
#     def _validate_token(self, token):
#         user = self._get_user_by_token(token)
#         if not user:
#             raise serializers.ValidationError("Токен недействителен или истёк срок его действия.")
#
#     def _get_user_by_token(self, token):
#         for user in User.objects.all():
#             if default_token_generator.check_token(user, token):
#                 return user
#         return None


# USER DATA
class UserDataSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    full_name = serializers.CharField(read_only=True)
    institution = serializers.CharField(read_only=True)
    department = serializers.CharField(read_only=True)
    position = serializers.CharField(read_only=True)
    orcid_id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    role = serializers.CharField(read_only=True)
    citation_count = serializers.IntegerField(read_only=True)
    h_index = serializers.IntegerField(read_only=True)
    profile_url = serializers.URLField(read_only=True)


# USER-PROFILE
class UserProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = UserDataSerializer(read_only=True)
    bio = serializers.CharField()
    research_interests = serializers.CharField()
    avatar = serializers.ImageField()
    website = serializers.URLField()
    google_scholar = serializers.URLField()
    researchgate = serializers.URLField()
    linkedin = serializers.URLField()
    twitter = serializers.URLField()
    followers_count = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)
    projects_count = serializers.IntegerField(read_only=True)
    publications_count = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()
