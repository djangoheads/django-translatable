import hashlib
import random
import pytest
from django.core.cache import cache as django_cache
import django

# renamed to avoid name conflict with pytest fixtures

from django.core.management import call_command
from dragoman.fixtures import countries, cities, regions
from django.conf import settings as django_settings
from dragoman.settings import TRANSLATION_DISPATCHER
from tests.test_django_project.settings import INSTALLED_APPS


# initialize django settings
def pytest_configure():
    django_settings.configure(
        INSTALLED_APPS=INSTALLED_APPS,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        STATIC_ROOT="/tmp/static/",  # noqa: S108
        STATIC_URL="/static/",
        MEDIA_URL="/media/",
        SECRET_KEY=hashlib.md5(str(random.random()).encode()).hexdigest(),  # noqa: S324, S311
        PREFIX="field://",
        TRANSLATE_FIELDS_NAME="translate_fields",
        TRANSLATION_DISPATCHER=TRANSLATION_DISPATCHER,
    )

    django.setup()


@pytest.fixture(autouse=True)
def dj_cache():
    """Fixture for django cache."""
    django_cache.clear()
    yield django_cache
    django_cache.clear()


@pytest.mark.django_db
def setup_models():
    from tests.test_django_project.models import TCountry, TCity, TRegion

    country_models = [TCountry(**country) for country in countries]
    country_instances = TCountry.objects.bulk_create(country_models)

    for city, country in zip(cities, country_instances):
        TCity.objects.create(pk=city["pk"], name=city["name"], population=city["population"], country=country)

    east = TRegion.objects.create(pk=regions[0]["pk"], name=regions[0]["name"])
    east.countries.set(TCountry.objects.filter(pk__in=regions[0]["countries"]))

    west = TRegion.objects.create(pk=regions[1]["pk"], name=regions[1]["name"])
    west.countries.set(TCountry.objects.filter(pk__in=regions[1]["countries"]))


@pytest.fixture(scope="session", autouse=True)
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("migrate")
        setup_models()
