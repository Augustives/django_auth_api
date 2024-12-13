import uuid

from django.db import models

from apps.address.models import Address
from apps.profile_app.constants import DocumentType, Gender
from apps.user.models import User


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    name = models.CharField(null=False, blank=False, max_length=256)
    birth_date = models.DateField(null=False, blank=False)
    gender = models.CharField(
        null=False, blank=False, max_length=1, choices=Gender.choices
    )

    document = models.CharField(null=False, blank=False, max_length=14)
    document_type = models.CharField(
        null=False, blank=False, max_length=4, choices=DocumentType.choices
    )
    address = models.ForeignKey(
        Address, verbose_name="Addresses", on_delete=models.PROTECT
    )

    def __str__(self):
        return self.user.email

    def user_email(self):
        return self.user.email

    def user_type(self):
        return self.user.user_type

    user_email.short_description = "User Email"
    user_type.short_description = "User Type"
