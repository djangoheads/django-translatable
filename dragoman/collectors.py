from typing import List

from django.db.models import Model
from django.conf import settings


class DjangoModelCollector:
    def __init__(self):
        self.result = []

    def collect_field(self, name, model: Model):
        meta = model._meta
        path = f"{settings.PREFIX}{meta.app_label}/{meta.model_name}/{model.pk}/{name}/"
        value = getattr(model, name, None)
        self.result.append((path, value))

    def collect_model(self, model: Model, translate_fields: List[str]):
        for field_name in translate_fields:
            self.collect_field(field_name, model)
