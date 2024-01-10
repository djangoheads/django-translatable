from django.db import models
from django.core.validators import RegexValidator


class TestCountry(models.Model):
    translate_fields = ["name"]

    name = models.CharField(max_length=255, verbose_name="Country name", help_text="Provide a name")

    code = models.CharField(
        "Country code",
        primary_key=True,
        max_length=2,
        validators=[
            RegexValidator(
                regex="^[A-Z]{2}$", message="Country code must be a 2 letter code", code="invalid_country_code"
            )
        ],
        unique=True,
    )

    class Meta:
        verbose_name = "country"
        verbose_name_plural = "countries"
        ordering = ["name"]
