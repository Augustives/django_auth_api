from allauth.account.utils import user_pk_to_url_str
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import PasswordResetSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.profile_app.models import Profile
from apps.profile_app.serializers import ProfileSerializer
from apps.user.models import User
from utils.serializer_fields import LowerEmailField

User = get_user_model()


class CustomPasswordResetSerializer(PasswordResetSerializer):
    def save(self):
        def custom_url_generator(request, user, token):
            """Generate a custom reset URL pointing to the frontend."""
            uid = user_pk_to_url_str(user)
            return f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

        request = self.context.get("request")

        opts = {
            "use_https": request.is_secure(),
            "from_email": getattr(settings, "DEFAULT_FROM_EMAIL", None),
            "request": request,
            "url_generator": custom_url_generator,
        }

        self.reset_form.save(**opts)


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    profile = serializers.JSONField(write_only=True)  # Accept profile data as JSON

    def validate_email(self, email):
        """Custom email validation to ensure uniqueness."""
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return email

    def get_cleaned_data(self):
        """Include profile data in the cleaned data."""
        data = super().get_cleaned_data()
        data["profile"] = self.validated_data.get("profile", {})
        return data

    def save(self, request):
        user = super().save(request)
        profile_data = self.cleaned_data.get("profile")

        profile_serializer = ProfileSerializer(data=profile_data)
        if profile_serializer.is_valid(raise_exception=True):
            Profile.objects.create(
                user=user, defaults=profile_serializer.validated_data
            )

        return user


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    email = LowerEmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ("id", "email", "password", "profile")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        profile_data = validated_data.pop("profile", None)

        user = User.objects.create(**validated_data)

        profile_serializer = ProfileSerializer(
            data=profile_data, context={"user": user}
        )
        if profile_serializer.is_valid(raise_exception=True):
            profile_serializer.save()

        return user
