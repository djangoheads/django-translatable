import pytest
from functools import partial
import django.apps
from django.conf import settings

from .mocks import ModelMockUtils, DjangoModelMockPatcher, TranslationMockVault
from test_django_project.signals import patch_translation
from test_django_project.models import TCountry, TRegion

from django.db.models.signals import post_init, pre_save
from tests.mocks import TranslationMockProvider


@pytest.mark.django_db
def test_collector():
    """Test the collector's logic on the mocked models"""

    instances = ModelMockUtils.get_instances(TCountry)

    for instance in instances:
        ModelMockUtils.update_source_translation_by_instance(instance)


@pytest.mark.django_db
def test_patcher():
    provider = TranslationMockProvider(TranslationMockVault)
    instances = ModelMockUtils.get_instances(TCountry)

    for instance in instances:
        DjangoModelMockPatcher(provider).patch_model(instance, "ru")

    for instance in instances:
        path = provider.get_path(instance, "name")
        assert provider.get(path, "ru") == instance.name


@pytest.mark.django_db
def test_models():
    models = [model for model in django.apps.apps.get_models() if hasattr(model, settings.TRANSLATE_FIELDS_NAME)]

    for model in models:
        post_init.connect(receiver=partial(patch_translation, direction="ru"), sender=model, weak=False)
        pre_save.connect(receiver=partial(patch_translation, direction="en"), sender=model, weak=False)

    region = TRegion.objects.filter(name="East").first()
    country_names = [country.name for country in region.countries.all()]

    assert country_names == ["Казахстан", "Таиланд"]

    countries = []
    for country in region.countries.all():
        country.save()
        countries.append(country)

    country_names = [country.name for country in countries]
    assert country_names == ["Kazakhstan", "Thailand"]
