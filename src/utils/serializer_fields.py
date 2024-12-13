from rest_framework import serializers


class LowerEmailField(serializers.EmailField):
    def to_internal_value(self, data):
        email = super().to_internal_value(data)
        return email.lower()
