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
    def update_source_translation_by_instance(cls, instance: Model, translate_fields: List[str]):
        collector = DjangoModelCollector()
        collector.collect_model(instance, translate_fields)
        for key, source in collector.result:
            cls.update_source_translation(key, source)

    @classmethod
    def update_source_translation(cls, key: str, source: str, provider: str = "default"):
        if not source:
            return


class TranslationVault:
    @classmethod
    def get_inner_vault(cls) -> dict:
        return {}


class TranslationProvider:
    def __init__(self, vault: TranslationVault):
        self.vault = vault

    def get(self, path: str, lang: str):
        inner_vault = self.vault.get_inner_vault()
        return inner_vault.get(path)[lang]

    def set(self):
        pass

    @classmethod
    def get_path(cls, model: Model, field_name: str) -> str:
        return f"{settings.PREFIX}{model._meta.app_label}/{model._meta.model_name}/{model.pk}/{field_name}"
