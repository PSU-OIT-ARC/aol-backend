from django.contrib.auth import get_user_model

from social_core.exceptions import AuthForbidden


def has_existing_account(backend, details, response, *args, **kwargs):
    user, email = (kwargs.get('user', None),
                   details.get('email', None))

    # Associations for anonymous user must match an existing email
    if user is None and not get_user_model().objects.filter(email=email).exists():
        raise AuthForbidden(backend)
