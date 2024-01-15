from django.core.management.base import BaseCommand
from dragoman.utils.common_utils import ModelUtils


class Command(BaseCommand):
    help = "Collect the model fields to translate"

    def add_arguments(self, parser):
        parser.add_argument("models", nargs="*", type=str)

    def handle(self, *args, **options):
        ModelUtils.collect_models()
