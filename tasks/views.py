from django.core.cache import cache
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.permissions.task_permissions import IsTaskProjectOwner

from .models import Task
from .serializers import TaskSerializer
from .tasks import notify_task_assignment


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

    def _clear_user_task_cache(self, user):
        """
        Supprime le cache de la liste des tâches pour l'utilisateur spécifié.
        """
        cache_key = f"tasks:list:user:{user.pk}"
        cache.delete(cache_key)

    def list(self, request, *args, **kwargs):
        """
        Retourne la liste des tâches avec mise en cache Redis.
        """
        cache_key = f"tasks:list:user:{request.user.pk}"

        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return Response(cached_data, status=status.HTTP_200_OK)

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        cache.set(cache_key, serializer.data, timeout=300)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        """
        Invalide le cache après la création d'une tâche.
        """
        super().perform_create(serializer)
        self._clear_user_task_cache(self.request.user)

    def perform_update(self, serializer):
        """
        Invalide le cache après la mise à jour d'une tâche
        et déclenche la notification asynchrone si une
        affectation est effectuée.
        """
        task = serializer.save()

        self._clear_user_task_cache(self.request.user)

        if task.assigned_to_id is not None:
            notify_task_assignment.delay(
                task_id=task.pk,
                user_id=task.assigned_to_id,
            )

    def perform_destroy(self, instance):
        """
        Invalide le cache après la suppression d'une tâche.
        """
        super().perform_destroy(instance)
        self._clear_user_task_cache(self.request.user)
