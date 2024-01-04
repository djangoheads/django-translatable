import os
from typing import Any, Dict, Tuple

from django.contrib.auth.models import User
from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    """Init Django command."""

    help = "Init Django (create caches, migrate, create admin user, " "collect static)."

    def handle(self, *args: Tuple[Any, ...], **options: Dict[str, Any]) -> None:
        """Init Django implementation."""
        call_command("createcachetable")

        call_command("migrate", no_input=True)

        if User.objects.all().count() == 0:
            User.objects.create_user("admin", password="admin")  # pragma: allowlist secret

        is_static_interacive = os.environ.get("RUNNING_TESTS", None) != "true"
        call_command("collectstatic", interactive=is_static_interacive)
