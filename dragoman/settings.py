from django.conf import settings

settings.TRANSLATION_DISPATCHER = {"models": {"TCountry": {"langs": ["en", "ru"], "translate_fields": ["name"]}}}
settings.TRANSLATE_FIELDS_NAME = "translate_fields"
