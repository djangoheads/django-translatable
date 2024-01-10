from django.conf import settings
from django.db.models import Model


class DjangoModelPatcher:
    def __init__(self, model: Model, translation):
        self.model = model
        self.translation = translation

    def patch_field(self, name):
        meta = self.model._meta
        path = f"{settings.PREFIX}{meta.app_label}/{meta.model_name}/{self.model.pk}/{name}/"
        translation = self.translation.get(path) or self.translation.get(path.rstrip("/"))
        if not translation:
            return
        setattr(self.model, name, translation)

    def patch(self):
        if hasattr(self.model, "translate_fields"):
            for field_name in self.model.translate_fields:
                self.patch_field(field_name)
