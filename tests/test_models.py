import pytest
from django.conf import settings
from django.core.management import call_command

from dragoman.patchers import DjangoModelPatcher
from dragoman.utils.provider_utils import TranslationProvider
from .mocks import ModelMockUtils
from tests.test_django_project.models import TCountry


@pytest.mark.django_db
def test_collector():
    """Test the collector's logic on the mocked models"""

    tr_dispatcher = settings.TRANSLATION_DISPATCHER
    instances = ModelMockUtils.get_instances(TCountry)

    for instance in instances:
        translate_fields = tr_dispatcher["models"][instance._meta.object_name][settings.TRANSLATE_FIELDS_NAME]
        ModelMockUtils.update_source_translation_by_instance(instance, translate_fields)


@pytest.mark.django_db
def test_patcher():
    tr_dispatcher = settings.TRANSLATION_DISPATCHER
    provider = TranslationProvider()
    instances = ModelMockUtils.get_instances(TCountry)

    for instance in instances:
        translate_fields = tr_dispatcher["models"][instance._meta.object_name][settings.TRANSLATE_FIELDS_NAME]
        DjangoModelPatcher(provider).patch_model(instance, translate_fields, "ru")

    for instance in instances:
        path = provider.get_path(instance, "name")
        assert provider.get(path, "ru") == instance.name


@pytest.mark.django_db
def test_collect_models():
    call_command("collect_models")
