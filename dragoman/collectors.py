from django.db.models import Model
from django.conf import settings


class DjangoModelCollector:
    def __init__(self, model: Model):
        self.model = model
        self.result = []

    def collect_field(self, name):
        meta = self.model._meta
        path = f"{settings.PREFIX}{meta.app_label}/{meta.model_name}/" f"{self.model.pk}/{name}/"
        value = getattr(self.model, name, None)
        self.result.append((path, value))

    def collect(self):
        for field_name in getattr(self.model, settings.TRANSLATE_FIELDS_NAME):
            self.collect_field(field_name)
