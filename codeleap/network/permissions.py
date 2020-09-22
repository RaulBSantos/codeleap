from rest_framework import permissions
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey, OneToOneField


class IsOwner(permissions.BasePermission):
    """
    This permission looks for ForeignKey and OneToOneField relations that uses
    `django.contrib.auth.models.User` as owner of an obj instance of model.
    """

    def has_object_permission(self, request, view, obj):
        for field in obj._meta.get_fields():
            # If case of other relations, just include the check for other instance types above
            if isinstance(field, ForeignKey) or isinstance(field, OneToOneField):
                user_field = getattr(obj, field.verbose_name)
                if isinstance(user_field, User):
                    return request.user == user_field
