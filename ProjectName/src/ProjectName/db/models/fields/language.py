from django.db.models.fields import CharField
from django.conf import settings


class LanguageField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 3)
        kwargs.setdefault('choices', settings.LANGUAGES)

        super(CharField, self).__init__(*args, **kwargs)
