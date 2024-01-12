from typing import List

from django.db.models import Model

from dragoman.utils.provider_utils import TranslationProvider


class DjangoModelCollector:
    def __init__(self, provider: TranslationProvider):
        self.provider = provider
        self.result = []

    def collect_field(self, name, model: Model):
        path = self.provider.get_path(model, field_name=name)
        value = getattr(model, name, None)
        self.result.append((path, value))

    def collect_model(self, model: Model, translate_fields: List[str]):
        for field_name in translate_fields:
            self.collect_field(field_name, model)
