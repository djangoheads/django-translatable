import pytest
from django.conf import settings

from .fixtures import translation
from .mocks import ModelMockUtils, DjangoModelMockPatcher

from test_django_project.models import TestCountry


def test_collector():
    """Test the collector's logic on the mocked models"""

    instances = ModelMockUtils.get_instances(TestCountry)

    for instance in instances:
        ModelMockUtils.update_source_translation_by_instance(instance)


def test_patcher():
    instances = ModelMockUtils.get_instances(TestCountry)

    for instance in instances:
        DjangoModelMockPatcher(instance, translation).patch()

    for instance in instances:
        meta = instance._meta
        path = f"{settings.PREFIX}{meta.app_label}/{meta.model_name}/{instance.pk}/name"
        assert translation.get(path) == instance.name


@pytest.mark.django_db
def test_models():
    assert TestCountry.objects.all().count() == 5
