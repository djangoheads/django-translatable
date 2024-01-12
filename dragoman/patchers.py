from typing import List
from django.db.models import Model
from dragoman.utils import TranslationProvider


class DjangoModelPatcher:
    def __init__(self, provider: TranslationProvider):
        self.provider = provider

    def patch_field(self, name: str, model: Model, lang: str):
        path = self.provider.get_path(model, field_name=name)
        translation = self.provider.get(path, lang)

        if not translation:
            return

        setattr(model, name, translation)

    def patch_model(self, model: Model, translate_fields: List[str], lang: str):
        for field_name in translate_fields:
            self.patch_field(field_name, model, lang)
