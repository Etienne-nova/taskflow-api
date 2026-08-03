from rest_framework.permissions import BasePermission


class IsProjectOwner(BasePermission):
    """
    Autorise uniquement le propriétaire du projet.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
