from django.db import models
from django.core.validators import RegexValidator


class TCountry(models.Model):
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

    def __str__(self):
        return f"{self.name}"


class TCity(models.Model):
    name = models.CharField(max_length=255, verbose_name="City name", help_text="Provide a name")
    population = models.PositiveIntegerField(default=250000)
    country = models.ForeignKey(TCountry, verbose_name="City", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "city"
        verbose_name_plural = "cities"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class TRegion(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    countries = models.ManyToManyField(TCountry, related_name="regions", related_query_name="region")

    class Meta:
        verbose_name = "region"
        verbose_name_plural = "regions"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"
