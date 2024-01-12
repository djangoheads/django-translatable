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
    def update_source_translation_by_instance(cls, instance: Model):
        collector = DjangoModelCollector()
        collector.collect(instance)
        for key, source in collector.result:
            cls.update_source_translation(key, source)

    @classmethod
    def update_source_translation(cls, key: str, source: str, provider: str = "default"):
        if not source:
            return


class TranslationProvider:
    def get(self, path: str, lang: str):
        pass

    def set(self):
        pass

    def get_path(self, model: Model, field_name: str) -> str:
        return f"{settings.PREFIX}{model._meta.app_label}/{model._meta.model_name}/{model.pk}/{field_name}/"
