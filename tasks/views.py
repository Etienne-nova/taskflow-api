from rest_framework import viewsets

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    API CRUD des tâches.
    """

    serializer_class = TaskSerializer

    def get_queryset(self):
        """
        Retourne uniquement les tâches
        des projets appartenant à l'utilisateur connecté.
        """
        return Task.objects.filter(project__owner=self.request.user)