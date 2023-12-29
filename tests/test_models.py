import pytest
from django.test import TestCase
import tests.__setup_django__  # noqa: F401


@pytest.mark.django_db
def test_models_loading() -> None:
    """Tests the app has been loaded."""

    pass
