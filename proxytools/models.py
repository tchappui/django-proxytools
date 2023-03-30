from django.db import models
from django.contrib.auth import models as auth_models


class CastableToProxy:
    """Mixin permettant la conversion de type entre un modèle et sous-modèle proxy."""

    def cast(self, model, in_place=False):
        """Casts a model instance to an instance of a subclass proxy model or
        the reverse."""
        if not issubclass(model, models.Model):
            raise TypeError(
                "model must be a subclass of django.db.models.Model"
            )

        def _is_cast_possible(from_type, to_type):
            """Checks if a cast from from_type to to_type is possible."""
            conditions = [
                issubclass(from_type, to_type) and from_type._meta.proxy,
                issubclass(to_type, from_type) and to_type._meta.proxy,
            ]
            return any(conditions)

        if _is_cast_possible(type(self), model):
            if in_place:
                self.__class__ = model
                return self
            else:
                return model.objects.get(pk=self.pk)
        else:
            raise TypeError(
                f"{self.__class__.__name__} cannot be converted to a {model.__name__}"
            )

    @classmethod
    def is_proxy(cls):
        """Returns True is the current class is a proxy model."""
        return cls._meta.proxy
