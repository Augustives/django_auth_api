from datetime import date

from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.address.serializers import AddressSerializer
from apps.profile_app.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    first_name = serializers.CharField(
        validators=[
            RegexValidator(
                regex="^[a-zA-Z]*$", message=_("First name must contain only letters")
            )
        ]
    )
    last_name = serializers.CharField(
        validators=[
            RegexValidator(
                regex="^[a-zA-Z]*$", message=_("Last name must contain only letters")
            )
        ]
    )

    class Meta:
        model = Profile
        fields = [
            "id",
            "address",
            "first_name",
            "last_name",
            "birth_date",
            "gender",
            "document",
            "document_type",
        ]

    def validate_birth_date(self, value):
        today = date.today()
        age = (
            today.year
            - value.year
            - ((today.month, today.day) < (value.month, value.day))
        )

        if age < 18 or age > 120:
            raise serializers.ValidationError(
                _("Age must be between 18 and 120 years.")
            )

        return value

    def create(self, validated_data):
        user = self.context.get("user")

        address_data = validated_data.pop("address")
        address_serializer = AddressSerializer(data=address_data)
        if address_serializer.is_valid(raise_exception=True):
            address = address_serializer.save()

        user_profile = Profile.objects.create(
            user=user, address=address, **validated_data
        )

        return user_profile

    def update(self, instance, validated_data):
        address_data = validated_data.pop("address", {})
        address = instance.address

        address_serializer = AddressSerializer(address, data=address_data, partial=True)
        if address_serializer.is_valid(raise_exception=True):
            address_serializer.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
