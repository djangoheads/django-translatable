from django.core.management.base import BaseCommand
from django.conf import settings

from dragoman.utils import ModelUtils


class Command(BaseCommand):
    help = 'Collect the model fields to translate'

    def add_arguments(self, parser):
        parser.add_argument('models', nargs='*', type=str)

    def handle(self, *args, **options):
        models = ModelUtils.get_models()

        for model in models:
            for instance in model.objects.all():
                ModelUtils.update_source_translation_by_instance(instance)
