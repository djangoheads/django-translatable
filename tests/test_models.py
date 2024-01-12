import pytest
from functools import partial
import django.apps
from django.conf import settings

from .mocks import ModelMockUtils, DjangoModelMockPatcher
from test_django_project.signals import patch_translation
from test_django_project.models import TCountry, TRegion

from django.db.models.signals import post_init, pre_save
from tests.fixtures import translation


@pytest.mark.django_db
def test_collector():
    """Test the collector's logic on the mocked models"""

    instances = ModelMockUtils.get_instances(TCountry)

    for instance in instances:
        ModelMockUtils.update_source_translation_by_instance(instance)


@pytest.mark.django_db
def test_patcher():
    instances = ModelMockUtils.get_instances(TCountry)

    for instance in instances:
        DjangoModelMockPatcher(translation).patch_model(instance)

    for instance in instances:
        meta = instance._meta
        path = f"{settings.PREFIX}{meta.app_label}/{meta.model_name}/{instance.pk}/name"
        assert translation.get(path) == instance.name


@pytest.mark.django_db
def test_models():
    models = [model for model in django.apps.apps.get_models() if hasattr(model, settings.TRANSLATE_FIELDS_NAME)]

    for model in models:
        post_init.connect(receiver=partial(patch_translation, direction="straight"), sender=model, weak=False)
        pre_save.connect(receiver=partial(patch_translation, direction="back"), sender=model, weak=False)

    region = TRegion.objects.filter(name="East").first()
    country_names = [country.name for country in region.countries.all()]

    assert country_names == ["Казахстан", "Таиланд"]

    countries = []
    for country in region.countries.all():
        country.save()
        countries.append(country)

    country_names = [country.name for country in countries]
    assert country_names == ["Kazakhstan", "Thailand"]
