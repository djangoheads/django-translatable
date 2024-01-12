from django.conf import settings
from django.db.models import Model

from dragoman.fixtures import translation


class TranslationProvider:
    def get(self, path: str, lang: str):
        return translation.get(path)[lang]

    def set(self):
        pass

    @classmethod
    def get_path(cls, model: Model, field_name: str) -> str:
        return f"{settings.PREFIX}{model._meta.app_label}/{model._meta.model_name}/{model.pk}/{field_name}"
