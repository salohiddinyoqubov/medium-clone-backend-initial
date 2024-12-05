"""
Module containing custom permission classes.
"""

from rest_framework.permissions import BasePermission, SAFE_METHODS


class OnlyOwnerPermission(BasePermission):
    """
    Custom permission to allow only the owner of the object to perform unsafe actions.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        if request.method in ["DELETE", "PATCH"]:
            return request.user.id == obj.author.id

        return False
