from django.conf import settings
from django.core.exceptions import PermissionDenied

from arcutils.cas.backends import CASModelBackend
from arcutils.ldap import escape, ldapsearch


def in_allowed_groups(username):
    uid = escape(username)
    groups = ' '.join('(cn={group})'.format(group=g) for g in settings.ALLOWED_LOGIN_GROUPS)
    query = '(& (memberUid={uid}) (| {groups}))'
    query = query.format_map(locals())
    results = ldapsearch(query)
    return bool(results)


class AOLCASModelBackend(CASModelBackend):

    def get_or_create_user(self, cas_data):
        if not in_allowed_groups(cas_data['username']):
            raise PermissionDenied('You are not allowed to log in to this site.')
        return super().get_or_create_user(cas_data, is_staff=True)
