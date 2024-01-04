from django.db.models import Model
from django.conf import settings
from typing import TypeVar, Type

T = TypeVar("T")


class DjangoModelCollector:
    def __init__(self, model: Model):
        self.model = model
        self.result = []

    def collect_field(self, name):
        meta = self.model._meta
        path = f"{settings.PREFIX}{meta.app_label}/{meta.model_name}/{self.model.pk}/{name}/"
        value = getattr(self.model, name, None)
        self.result.append((path, value))

    def collect(self):
        for field_name in getattr(self.model, settings.TRANSLATE_FIELDS_NAME):
            self.collect_field(field_name)


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
