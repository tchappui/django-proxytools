from functools import wraps

from django.contrib.auth import get_user_model
from .models import CastableToProxy


def user_proxy_required(user_type):
    """Decorator used to convert request.user to a proxy subtype."""
    if not issubclass(user_type, get_user_model()):
        raise TypeError("user_type must be a subtype of AUTH_USER_MODEL")
    elif not issubclass(user_type, CastableToProxy):
        raise TypeError("user_type must be castable to a proxy model")
    elif not user_type.is_proxy():
        raise TypeError("user_type must be a proxy model")

    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                request.user.cast(user_type, in_place=True)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator
