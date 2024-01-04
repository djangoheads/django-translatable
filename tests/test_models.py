import tests.__setup_django__  # noqa: F401
from dragoman.utils import ModelMockUtils


def test_models_loading() -> None:
    """Tests the app has been loaded."""

    models = ModelMockUtils.get_models()

    for model in models:
        ModelMockUtils.update_source_translation_by_instance(model())
