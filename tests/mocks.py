from django.conf import settings
from .fixtures import countries
from typing import TypeVar, Type, List

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


class ModelMockUtils:
    @classmethod
    def get_models(cls) -> List[Type[T]]:
        return [type("Country", (), country) for country in countries]

    @classmethod
    def update_source_translation_by_instance(cls, instance: Type[T]):
        collector = DjangoModelMockCollector(instance)
        collector.collect()
        for key, source in collector.result:
            cls.update_source_translation(key, source)

    @classmethod
    def update_source_translation(cls, key: str, source: str, provider: str = "default"):
        assert source is not None
        assert source != ""
