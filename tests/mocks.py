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


class TranslationMockProvider(TranslationProvider):
    def __init__(self, vault: TranslationMockVault):
        self.vault = vault

    def get(self, path: str, lang: str):
        inner_vault = self.vault.get_inner_vault()
        return inner_vault.get(path)[lang]

    def set(self):
        pass

    @classmethod
    def get_path(cls, model: Model, field_name: str) -> str:
        return f"{settings.PREFIX}{model._meta.app_label}/{model._meta.model_name}/{model.pk}/{field_name}"


class DjangoModelMockCollector:
    def __init__(self, provider: TranslationMockProvider):
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


class DjangoModelMockPatcher:
    def __init__(self, provider: TranslationMockProvider):
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
