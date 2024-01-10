from django.conf import settings
from django.db.models import QuerySet, Model

from dragoman.collectors import DjangoModelCollector
from typing import TypeVar, Type

T = TypeVar("T")


class DjangoModelMockCollector:
    def __init__(self, mock_model: Type[T]):
        self.mock_model = mock_model
        self.result = []

    def collect_field(self, name):
        path = f"{settings.PREFIX}{self.mock_model.app_label}/{self.mock_model.model_name}/{self.mock_model.pk}/{name}/"
        value = getattr(self.mock_model, name, None)
        self.result.append((path, value))

    def collect(self):
        for field_name in getattr(self.mock_model, settings.TRANSLATE_FIELDS_NAME):
            self.collect_field(field_name)


class DjangoModelMockPatcher:
    def __init__(self, model: Type[T], translation: dict):
        self.model = model
        self.translation = translation

    def patch_field(self, name: str):
        meta = self.model._meta
        path = f"{settings.PREFIX}{meta.app_label}/{meta.model_name}/{self.model.pk}/{name}/"
        translation = self.translation.get(path) or self.translation.get(path.rstrip("/"))
        if not translation:
            return
        setattr(self.model, name, translation)

    def patch(self):
        for field_name in self.model.translate_fields:
            self.patch_field(field_name)


class ModelMockUtils:
    @classmethod
    def get_instances(cls, model: Type[Model]) -> QuerySet[Type[Model]]:
        return model.objects.all()

    @classmethod
    def update_source_translation_by_instance(cls, instance: Type[T]):
        collector = DjangoModelCollector(instance)
        collector.collect()
        for key, source in collector.result:
            cls.update_source_translation(key, source)

    @classmethod
    def update_source_translation(cls, key: str, source: str, provider: str = "default"):
        assert source is not None
        assert source != ""
