from django.conf import settings
from django.core.management.base import BaseCommand
from dragoman.utils.common_utils import ModelUtils


class Command(BaseCommand):
    help = "Collect the model fields to translate"

    def add_arguments(self, parser):
        parser.add_argument("models", nargs="*", type=str)

    def handle(self, *args, **options):
        models = ModelUtils.get_models()

        tr_dispatcher = settings.TRANSLATION_DISPATCHER

        for model in models:
            for instance in model.objects.all():
                translate_fields = tr_dispatcher["models"][instance._meta.object_name][settings.TRANSLATE_FIELDS_NAME]
                ModelUtils.update_source_translation_by_instance(instance, translate_fields)
