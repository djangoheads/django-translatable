from django.conf import settings
from django.db.models import Model


class DjangoModelPatcher:
    def __init__(self, provider: dict):
        self.provider = provider

    def patch_field(self, name: str, model: Model):
        meta = model._meta
        path = f"{settings.PREFIX}{meta.app_label}/{meta.model_name}/{model.pk}/{name}/"
        translation = self.provider.get(path) or self.provider.get(path.rstrip("/"))

        if not translation:
            return

        setattr(model, name, translation)

    def patch_model(self, model: Model):
        if hasattr(model, settings.TRANSLATE_FIELDS_NAME):
            for field_name in getattr(model, settings.TRANSLATE_FIELDS_NAME):
                self.patch_field(field_name, model)
