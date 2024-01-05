import django.apps
from typing import Type, List, TypeVar
from django.conf import settings
from django.db.models import Model
from dragoman.collectors import DjangoModelCollector

T = TypeVar("T")


class ModelUtils:
    @classmethod
    def get_models(cls) -> List[Type[Model]]:
        return [model for model in django.apps.apps.get_models() if hasattr(model, settings.TRANSLATE_FIELDS_NAME)]

    @classmethod
    def update_source_translation_by_instance(cls, instance: Type[Model]):
        collector = DjangoModelCollector(instance)
        collector.collect()
        for key, source in collector.result:
            cls.update_source_translation(key, source)

    @classmethod
    def update_source_translation(cls, key: str, source: str, provider: str = "default"):
        if not source:
            return
