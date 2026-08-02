from rest_framework.permissions import BasePermission


class IsTaskProjectOwner(BasePermission):
    """
    Autorise uniquement le propriétaire
    du projet auquel appartient la tâche.
    """

    def has_object_permission(self, request, view, obj):
        return obj.project.owner == request.user