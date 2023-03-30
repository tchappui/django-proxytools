from django.contrib.auth import get_user_model
from .models import CastableToProxy


class UserProxyRequiredMixin:
    """Mixin used to convert request.user to a proxy subtype."""

    user_proxy_type = None

    def dispatch(self, request, *args, **kwargs):
        if not issubclass(self.user_proxy_type, get_user_model()):
            raise TypeError(
                "user_proxy_type must be a subtype of AUTH_USER_MODEL"
            )
        elif not issubclass(self.user_proxy_type, CastableToProxy):
            raise TypeError("user_type must be castable to a proxy model")
        elif not self.user_proxy_type.is_proxy():
            raise TypeError("user_type must be a proxy model")
        if request.user.is_authenticated:
            request.user.cast(self.user_proxy_type, in_place=True)
        return super().dispatch(request, *args, **kwargs)
