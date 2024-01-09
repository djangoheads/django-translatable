from django.apps import apps
from django.conf import settings
from django.test import TestCase

from dragoman.apps import DragomanConfig


class TestDragomanConfig(TestCase):
    """Tests for DragomanConfig."""

    def test_app_loading(self) -> None:
        """Tests the app has been loaded."""
        self.assertIn("dragoman", settings.INSTALLED_APPS)
        app_config = apps.get_app_config("dragoman")
        self.assertIsInstance(app_config, DragomanConfig)
