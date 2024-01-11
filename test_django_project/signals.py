from django.conf import settings

from tests.fixtures import translation


def patch_translation(sender, instance, **kwargs):
    meta = instance._meta
    path = f"{settings.PREFIX}{meta.app_label}/{meta.model_name}/{instance.pk}/name"

    tr = translation.get(path)[kwargs["direction"]]
    if not tr:
        return
    setattr(instance, "name", tr)
