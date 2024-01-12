from django.conf import settings
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

    def patch_model(self, model: Model, lang: str):
        translate_fields = (
            getattr(model, settings.TRANSLATE_FIELDS_NAME) if hasattr(model, settings.TRANSLATE_FIELDS_NAME) else []
        )

        for field_name in translate_fields:
            self.patch_field(field_name, model, lang)
