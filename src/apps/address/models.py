import uuid

from django.db import models

from apps.address.constants import Country


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    country = models.CharField(
        null=False, blank=False, max_length=2, choices=Country.choices
    )
    state = models.CharField(max_length=128, null=False, blank=False)
    city = models.CharField(max_length=128, null=False, blank=False)

    postal_code = models.CharField(max_length=32, null=False, blank=False)
    address = models.CharField(max_length=128, null=False, blank=False)
    number = models.CharField(max_length=32, null=False, blank=False)
    additional_info = models.CharField(max_length=128, null=False, blank=True)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.postal_code}, {self.city}, {self.state}, {self.country}"
