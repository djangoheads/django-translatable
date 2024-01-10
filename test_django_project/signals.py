from typing import Type
from django.db.models.signals import post_init
from django.dispatch import receiver
from django.conf import settings

from tests.fixtures import translation
from .models import TCountry


@receiver(post_init, sender=TCountry, dispatch_uid="UNIQUE_COUNTRY_CONNECTION_UID")
def init_country(sender: Type[TCountry], instance: TCountry, **kwargs):
    meta = instance._meta
    path = f"{settings.PREFIX}{meta.app_label}/{meta.model_name}/{instance.pk}/name/"

    tr = translation.get(path) or translation.get(path.rstrip("/"))
    if not tr:
        return
    setattr(instance, "name", tr)
