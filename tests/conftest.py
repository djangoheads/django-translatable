import hashlib
import random
import pytest
from django.core.cache import cache as django_cache
import django

# renamed to avoid name conflict with pytest fixtures
from django.conf import settings as django_settings

from test_django_project.settings import INSTALLED_APPS
from django.core.management import call_command
from fixtures import countries


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
    )

    django.setup()


@pytest.fixture(autouse=True)
def dj_cache():
    """Fixture for django cache."""
    django_cache.clear()
    yield django_cache
    django_cache.clear()


def setup_countries():
    from test_django_project.models import TestCountry

    models = [TestCountry(**country) for country in countries]
    TestCountry.objects.bulk_create(models)


@pytest.fixture(scope="session", autouse=True)
def django_db_setup():
    call_command("migrate")
    setup_countries()
