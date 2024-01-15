import django.apps
from typing import Type, List
from django.conf import settings
from django.db.models import Model
from dragoman.collectors import DjangoModelCollector
from dragoman.utils.provider_utils import TranslationProvider


class ModelUtils:
    @classmethod
    def get_models(cls) -> List[Type[Model]]:
        return [model for model in django.apps.apps.get_models() if hasattr(model, settings.TRANSLATE_FIELDS_NAME)]

    @classmethod
    def collect_models(cls):
        models = ModelUtils.get_models()

        tr_dispatcher = settings.TRANSLATION_DISPATCHER

        for model in models:
            for instance in model.objects.all():
                translate_fields = tr_dispatcher["models"][instance._meta.object_name][settings.TRANSLATE_FIELDS_NAME]
                ModelUtils.update_source_translation_by_instance(instance, translate_fields)

    @classmethod
    def update_source_translation_by_instance(cls, instance: Model, translate_fields: List[str]):
        provider = TranslationProvider()
        collector = DjangoModelCollector(provider)
        collector.collect_model(instance, translate_fields)
        for key, source in collector.result:
            cls.update_source_translation(key, source)

    @classmethod
    def update_source_translation(cls, key: str, source: str, provider: str = "default"):
        if not source:
            return
