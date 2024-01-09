from django.conf import settings

from .fixtures import translation
from .mocks import ModelMockUtils, DjangoModelMockPatcher


def test_collector():
    """Test the collector's logic on the mocked models"""

    instances = ModelMockUtils.get_instances()

    for instance in instances:
        ModelMockUtils.update_source_translation_by_instance(instance())


def test_patcher():
    instances = [instance() for instance in ModelMockUtils.get_instances()]

    for instance in instances:
        DjangoModelMockPatcher(instance, translation).patch()

    for instance in instances:
        path = f"{settings.PREFIX}{instance.app_label}/{instance.model_name}/{instance.pk}/name"
        assert translation.get(path) == instance.name
