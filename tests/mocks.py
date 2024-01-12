from django.conf import settings
from django.db.models import QuerySet, Model

from dragoman.collectors import DjangoModelCollector
from typing import TypeVar, Type
from dragoman.utils import TranslationProvider
from tests.fixtures import translation

T = TypeVar("T")


class TranslationMockVault:
    @classmethod
    def get_inner_vault(cls):
        return translation


class DjangoModelMockCollector:
    def __init__(self, provider: TranslationProvider):
        self.provider = provider
        self.result = []

    def collect_field(self, name, model: Model):
        meta = model._meta
        path = f"{settings.PREFIX}{meta.app_label}/{meta.model_name}/{model.pk}/{name}/"
        value = getattr(model, name, None)
        self.result.append((path, value))

    def collect_model(self, model: Model):
        for field_name in getattr(model, settings.TRANSLATE_FIELDS_NAME):
            self.collect_field(field_name, model)


class ModelMockUtils:
    @classmethod
    def get_instances(cls, model: Type[Model]) -> QuerySet[Type[Model]]:
        return model.objects.all()

    @classmethod
    def update_source_translation_by_instance(cls, instance: Model):
        collector = DjangoModelCollector()
        collector.collect_model(instance)
        for key, source in collector.result:
            cls.update_source_translation(key, source)

    @classmethod
    def update_source_translation(cls, key: str, source: str, provider: str = "default"):
        assert source is not None
        assert source != ""
