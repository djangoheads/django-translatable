import tests.__setup_django__  # noqa: F401
from .mocks import ModelMockUtils


def test_collector() -> None:
    """Test the collector's logic on the mocked models"""

    models = ModelMockUtils.get_models()

    for model in models:
        ModelMockUtils.update_source_translation_by_instance(model())
