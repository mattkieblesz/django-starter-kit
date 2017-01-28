from django.db import models

from .manager import BaseManager

__all__ = ('BaseModel', 'Model', 'sane_repr')


def sane_repr(*attrs):
    if 'id' not in attrs and 'pk' not in attrs:
        attrs = ('id',) + attrs

    def _repr(self):
        cls = type(self).__name__

        pairs = ('{}={}'.format(a, repr(getattr(self, a, None))) for a in attrs)

        return u'<{} at 0x{.x}: {}>'.format(cls, id(self), ', '.join(pairs))

    return _repr


class BaseModel(models.Model):
    class Meta:
        abstract = True

    objects = BaseManager()


class Model(BaseModel):
    class Meta:
        abstract = True

    __repr__ = sane_repr('id')
