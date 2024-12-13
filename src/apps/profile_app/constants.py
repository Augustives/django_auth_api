from django.db import models


class Gender(models.TextChoices):
    MALE = "M", "Male"
    FEMALE = "F", "Female"
    OTHER = "O", "Other"


class DocumentType(models.TextChoices):
    CPF = ("CPF",)
    CNPJ = ("CNPJ",)
