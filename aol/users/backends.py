from arcutils.ldap import escape, ldapsearch
from django.conf import settings
from django.contrib.auth import get_user_model
from djangocas.backends import CASBackend


class AOLBackend(CASBackend):
    """
    Only allows user in ALLOWED_LOGIN_GROUPS to login
    """
    def get_or_init_user(self, username):
        username = escape(username)
        query = "(& (| %s) (memberuid=%s))" % (" ".join("(cn=%s)" % g for g in settings.ALLOWED_LOGIN_GROUPS), username)
        results = ldapsearch(query)

        if len(results) == 0:
            return None

        User = get_user_model()

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            email = username + "@pdx.edu"
            user = User(email=email, username=username)

        user.is_active = True
        user.is_staff = True
        user.save()

        return user
