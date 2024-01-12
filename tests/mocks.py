from django.db.models import QuerySet, Model

from dragoman.collectors import DjangoModelCollector
from typing import TypeVar, Type, List
from tests.fixtures import translation

T = TypeVar("T")


class TranslationMockVault:
    @classmethod
    def get_inner_vault(cls):
        return translation


class ModelMockUtils:
    @classmethod
    def get_instances(cls, model: Type[Model]) -> QuerySet[Type[Model]]:
        return model.objects.all()

    @classmethod
    def update_source_translation_by_instance(cls, instance: Model, translate_fields: List[str]):
        collector = DjangoModelCollector()
        collector.collect_model(instance, translate_fields)
        for key, source in collector.result:
            cls.update_source_translation(key, source)

    @classmethod
    def update_source_translation(cls, key: str, source: str, provider: str = "default"):
        assert source is not None
        assert source != ""
