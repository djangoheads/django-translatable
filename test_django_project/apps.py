from django.apps import AppConfig


class TestConfig(AppConfig):
    """Test app config."""

    name = "test_django_project"
    verbose_name = "Test Django Project"
    default_auto_field = "django.db.models.BigAutoField"
