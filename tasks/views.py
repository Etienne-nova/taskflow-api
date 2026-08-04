from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.permissions.task_permissions import IsTaskProjectOwner

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    API CRUD des tâches.
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsTaskProjectOwner]

    def get_queryset(self):
        """
        Retourne uniquement les tâches des projets
        appartenant à l'utilisateur connecté en
        optimisant les relations avec la base.
        """
        return Task.objects.filter(project__owner=self.request.user).select_related(
            "project"
        )
